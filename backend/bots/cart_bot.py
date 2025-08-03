# # backend/bots/cart_bot.py

# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# import time

# from backend.bots.amazon_bot import add_to_cart_amazon
# from backend.bots.flipkart_bot import add_to_cart_flipkart
# from backend.bots.myntra_bot import add_to_cart_myntra

# def add_to_cart(product_list):
#     options = Options()
#     options.add_argument("--headless=false")
#     driver = webdriver.Chrome(options=options)

#     # 🔧 Fix starts here
#     if isinstance(product_list, str):
#         product_list = [{"url": product_list}]
#     elif isinstance(product_list, dict):
#         product_list = [product_list]
#     elif isinstance(product_list, list) and all(isinstance(item, str) for item in product_list):
#         product_list = [{"url": u} for u in product_list]
#     # 🔧 Fix ends here

#     for product in product_list:
#         url = product.get("url", "")
#         if "amazon" in url:
#             try:
#                 add_to_cart_amazon([url])
#             except Exception as e:
#                 print("❌ Amazon cart error:", e)

#         elif "flipkart" in url:
#             try:
#                 add_to_cart_flipkart(driver, url)
#             except Exception as e:
#                 print("❌ Flipkart cart error:", e)

#         elif "myntra" in url:
#             try:
#                 add_to_cart_myntra(driver, url)
#             except Exception as e:
#                 print("❌ Myntra cart error:", e)

#         else:
#             print("❌ Unknown platform:", url)

#     driver.quit()
#     return f"🛒 Added {len(product_list)} item(s) to cart."













# _________________________________________________________________________________________________














# backend/bots/cart_bot.py

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import pymysql
from pymysql.err import MySQLError as Error
from pymysql.cursors import DictCursor
from dotenv import load_dotenv
import os

from backend.bots.amazon_bot import add_to_cart_amazon
from backend.bots.flipkart_bot import add_to_cart_flipkart
from backend.bots.myntra_bot import add_to_cart_myntra

load_dotenv()

def get_product_details(driver, url):
    """Extract product details from the URL"""
    try:
        driver.get(url)
        time.sleep(3)  # Wait for page to load
        
        product_description = ""
        price = 0.0
        
        if "amazon" in url:
            try:
                # Amazon product title - multiple selectors for better reliability
                title_selectors = [
                    "#productTitle",
                    "h1.a-size-large",
                    "h1[data-automation-id='product-title']",
                    ".product-title"
                ]
                
                for selector in title_selectors:
                    try:
                        title_element = driver.find_element(By.CSS_SELECTOR, selector)
                        product_description = title_element.text.strip()
                        if product_description:  # Make sure we got actual text
                            break
                    except:
                        continue
                
                # Amazon price - try multiple selectors
                price_selectors = [
                    ".a-price-whole",
                    ".a-price .a-offscreen",
                    ".a-price-range .a-price .a-offscreen",
                    "#priceblock_dealprice",
                    "#priceblock_ourprice",
                    ".a-price.a-text-price.a-size-medium.apexPriceToPay .a-offscreen"
                ]
                
                for selector in price_selectors:
                    try:
                        price_element = driver.find_element(By.CSS_SELECTOR, selector)
                        price_text = price_element.text.replace(',', '').replace('₹', '').strip()
                        price = float(price_text.split()[0])
                        break
                    except:
                        continue
                        
            except Exception as e:
                print(f"❌ Error extracting Amazon details: {e}")
                
        elif "flipkart" in url:
            try:
                # Flipkart product title - comprehensive selectors
                title_selectors = [
                    "span.B_NuCI",           # Main product title
                    "h1.yhB1nd",             # Alternative title
                    "h1._35KyD6",            # Another variation
                    "h1[class*='_35KyD6']",  # Class pattern match
                    ".B_NuCI",               # Without span
                    "span[class*='B_NuCI']"  # Pattern match
                ]
                
                for selector in title_selectors:
                    try:
                        title_element = driver.find_element(By.CSS_SELECTOR, selector)
                        product_description = title_element.text.strip()
                        if product_description and len(product_description) > 5:  # Valid title
                            break
                    except:
                        continue
                
                # Flipkart price
                price_selectors = [
                    "div._30jeq3._16Jk6d",
                    "div._1_WHN1",
                    "div._25b18c"
                ]
                
                for selector in price_selectors:
                    try:
                        price_element = driver.find_element(By.CSS_SELECTOR, selector)
                        price_text = price_element.text.replace(',', '').replace('₹', '').strip()
                        price = float(price_text.split()[0])
                        break
                    except:
                        continue
                        
            except Exception as e:
                print(f"❌ Error extracting Flipkart details: {e}")
                
        elif "myntra" in url:
            try:
                # Myntra product title - comprehensive selectors
                title_selectors = [
                    "h1.pdp-title",          # Main title
                    "h1.pdp-name",           # Alternative
                    ".pdp-product-name",     # Product name class
                    "h1[class*='pdp']",      # Pattern match
                    ".product-title",        # Generic title
                    "h1.title"               # Simple title
                ]
                
                for selector in title_selectors:
                    try:
                        title_element = driver.find_element(By.CSS_SELECTOR, selector)
                        product_description = title_element.text.strip()
                        if product_description and len(product_description) > 5:  # Valid title
                            break
                    except:
                        continue
                
                # Myntra price
                price_selectors = [
                    "span.pdp-price",
                    "strong.pdp-price"
                ]
                
                for selector in price_selectors:
                    try:
                        price_element = driver.find_element(By.CSS_SELECTOR, selector)
                        price_text = price_element.text.replace(',', '').replace('₹', '').replace('Rs.', '').strip()
                        price = float(price_text.split()[0])
                        break
                    except:
                        continue
                        
            except Exception as e:
                print(f"❌ Error extracting Myntra details: {e}")
        
        # Fallback: if no description found, use a generic one
        if not product_description:
            if "amazon" in url:
                product_description = "Amazon Product"
            elif "flipkart" in url:
                product_description = "Flipkart Product"
            elif "myntra" in url:
                product_description = "Myntra Product"
            else:
                product_description = "Unknown Product"
        
        # Fallback: if no price found, set to 0
        if price == 0.0:
            print(f"⚠️ Could not extract price for {url}")
            
        return product_description, price
        
    except Exception as e:
        print(f"❌ Error getting product details from {url}: {e}")
        return "Product", 0.0

def save_to_database(user_id, product_description, product_url, price):
    """Save cart item to database"""
    conn = None
    try:
        conn = pymysql.connect(
            host="localhost",
            user="root",
            password="12345",
            database="shopbuddy",
            cursorclass=DictCursor,
            autocommit=True
        )
        cursor = conn.cursor()
        
        insert_query = """
        INSERT INTO cartadders (user_id, product_description, product_url, price) 
        VALUES (%s, %s, %s, %s)
        """
        
        cursor.execute(insert_query, (user_id, product_description, product_url, price))
        
        print(f"✅ Saved to database: {product_description} - ₹{price}")
        return True
        
    except Error as e:
        print(f"❌ Database error: {e}")
        return False
        
    finally:
        if conn and conn.open:
            cursor.close()
            conn.close()

def add_to_cart(product_list, user_id=None):
    """
    Add products to cart and save to database
    
    Args:
        product_list: List of products or single product URL
        user_id: User ID from cookies/session
    """
    if not user_id:
        print("❌ Error: user_id is required to save cart items")
        return "❌ Error: User not authenticated"
    
    options = Options()
    options.add_argument("--headless=false")  # Set to True for production
    driver = webdriver.Chrome(options=options)

    # 🔧 Fix starts here - normalize product_list format
    if isinstance(product_list, str):
        product_list = [{"url": product_list}]
    elif isinstance(product_list, dict):
        product_list = [product_list]
    elif isinstance(product_list, list) and all(isinstance(item, str) for item in product_list):
        product_list = [{"url": u} for u in product_list]
    # 🔧 Fix ends here

    successful_additions = 0
    
    for product in product_list:
        url = product.get("url", "")
        
        if not url:
            print("❌ No URL provided for product")
            continue
            
        print(f"🔍 Processing: {url}")
        
        # Get product details first
        product_description, price = get_product_details(driver, url)
        
        # Add to respective platform cart
        cart_success = False
        
        if "amazon" in url:
            try:
                add_to_cart_amazon([url])
                cart_success = True
                print(f"✅ Added to Amazon cart: {product_description}")
            except Exception as e:
                print(f"❌ Amazon cart error: {e}")

        elif "flipkart" in url:
            try:
                add_to_cart_flipkart(driver, url)
                cart_success = True
                print(f"✅ Added to Flipkart cart: {product_description}")
            except Exception as e:
                print(f"❌ Flipkart cart error: {e}")

        elif "myntra" in url:
            try:
                add_to_cart_myntra(driver, url)
                cart_success = True
                print(f"✅ Added to Myntra cart: {product_description}")
            except Exception as e:
                print(f"❌ Myntra cart error: {e}")

        else:
            print(f"❌ Unknown platform: {url}")
            continue
        
        # Save to database regardless of cart success (for tracking)
        if save_to_database(user_id, product_description, url, price):
            successful_additions += 1
            print(f"💾 Saved to database: {product_description}")
        else:
            print(f"❌ Failed to save to database: {product_description}")

    driver.quit()
    
    if successful_additions > 0:
        return f"🛒 Successfully processed {successful_additions} item(s). Added to cart and saved to database."
    else:
        return "❌ No items were successfully processed."


# Additional utility functions

def get_user_cart_items(user_id):
    """Get all cart items for a specific user"""
    conn = None
    try:
        conn = pymysql.connect(
            host="localhost",
            user="root",
            password="12345",
            database="shopbuddy",
            cursorclass=DictCursor,
            autocommit=True
        )
        cursor = conn.cursor()
        
        select_query = """
        SELECT id, product_description, product_url, price, timestamp 
        FROM cartadders 
        WHERE user_id = %s 
        ORDER BY timestamp DESC
        """
        
        cursor.execute(select_query, (user_id,))
        cart_items = cursor.fetchall()
        
        return cart_items
        
    except Error as e:
        print(f"❌ Database error: {e}")
        return []
        
    finally:
        if conn and conn.open:
            cursor.close()
            conn.close()

def remove_cart_item(item_id, user_id):
    """Remove a specific cart item"""
    conn = None
    try:
        conn = pymysql.connect(
            host="localhost",
            user="root",
            password="12345",
            database="shopbuddy",
            cursorclass=DictCursor,
            autocommit=True
        )
        cursor = conn.cursor()
        
        delete_query = """
        DELETE FROM cartadders 
        WHERE id = %s AND user_id = %s
        """
        
        cursor.execute(delete_query, (item_id, user_id))
        
        if cursor.rowcount > 0:
            print(f"✅ Removed cart item {item_id}")
            return True
        else:
            print(f"❌ Cart item {item_id} not found or doesn't belong to user")
            return False
            
    except Error as e:
        print(f"❌ Database error: {e}")
        return False
        
    finally:
        if conn and conn.open:
            cursor.close()
            conn.close()

def clear_user_cart(user_id):
    """Clear all cart items for a user"""
    conn = None
    try:
        conn = pymysql.connect(
            host="localhost",
            user="root",
            password="12345",
            database="shopbuddy",
            cursorclass=DictCursor,
            autocommit=True
        )
        cursor = conn.cursor()
        
        delete_query = "DELETE FROM cartadders WHERE user_id = %s"
        cursor.execute(delete_query, (user_id,))
        
        items_deleted = cursor.rowcount
        print(f"✅ Cleared {items_deleted} items from cart")
        return items_deleted
        
    except Error as e:
        print(f"❌ Database error: {e}")
        return 0
        
    finally:
        if conn and conn.open:
            cursor.close()
            conn.close()