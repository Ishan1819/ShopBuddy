from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from urllib.parse import quote_plus

def create_driver(headless=False):
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    if headless:
        options.add_argument("--headless=new")
    else:
        print("🟢 Headless mode is OFF — browser will be visible.")

    return webdriver.Chrome(options=options)


def extract_product_results(driver):
    """Extract product information from search results"""
    results = []
    
    # Multiple selectors for product containers
    product_selectors = [
        "//div[@data-component-type='s-search-result']",
        "//div[contains(@class, 's-result-item')]",
        "//div[@data-asin and @data-asin!='']"
    ]
    
    products = []
    for selector in product_selectors:
        try:
            products = driver.find_elements(By.XPATH, selector)
            if products:
                break
        except:
            continue
    
    print(f"📦 Found {len(products)} products")
    
    for i, product in enumerate(products[:15]):  # Get more results
        try:
            # Extract title with more comprehensive selectors
            title_selectors = [
                ".//h2//span[contains(@class, 'a-size-mini')]",
                ".//h2//span[contains(@class, 'a-size-base-plus')]",
                ".//h2//a//span",
                ".//h2//span",
                ".//a[contains(@class, 's-link-style')]//span",
                ".//span[contains(@class, 's-size-mini')]"
            ]
            
            title = None
            for title_sel in title_selectors:
                try:
                    title_elem = product.find_element(By.XPATH, title_sel)
                    title = title_elem.text.strip()
                    if title and len(title) > 10:  # Ensure we get meaningful title
                        break
                except:
                    continue
            
            # Extract link with better error handling
            link_selectors = [
                ".//h2//a[@href]",
                ".//a[contains(@class, 's-link-style')][@href]",
                ".//a[@href and contains(@href, '/dp/')]"
            ]
            
            link = None
            for link_sel in link_selectors:
                try:
                    link_elem = product.find_element(By.XPATH, link_sel)
                    raw_link = link_elem.get_attribute("href")
                    if raw_link:
                        # Clean and validate URL
                        if raw_link.startswith("http"):
                            link = raw_link
                        elif raw_link.startswith("/"):
                            link = f"https://www.amazon.in{raw_link}"
                        else:
                            link = f"https://www.amazon.in/{raw_link}"
                        
                        # Validate that it's a product URL
                        if "/dp/" in link or "/gp/product/" in link:
                            break
                        else:
                            link = None
                except Exception as e:
                    print(f"🔗 Link extraction error for selector {link_sel}: {e}")
                    continue
            
            # Extract price with better handling
            price_selectors = [
                ".//span[@class='a-price-whole']",
                ".//span[contains(@class, 'a-price-whole')]",
                ".//span[@class='a-offscreen']",
                ".//span[contains(@class, 'a-price')]//span[@aria-hidden='true']"
            ]
            
            price = None
            for price_sel in price_selectors:
                try:
                    price_elem = product.find_element(By.XPATH, price_sel)
                    price_text = price_elem.get_attribute("textContent") or price_elem.text
                    if price_text and any(char.isdigit() for char in price_text):
                        price = price_text.strip().replace(',', '')
                        break
                except:
                    continue
            
            # Additional validation and debugging
            if title and link:
                # Validate URL format
                if not any(pattern in link for pattern in ["/dp/", "/gp/product/", "amazon.in"]):
                    print(f"⚠️ Suspicious URL format: {link}")
                    continue
                
                # Clean up title
                title = title.replace('\n', ' ').strip()
                
                result = {
                    "title": title,
                    "url": link,
                    "price": price,
                    "position": i + 1
                }
                
                results.append(result)
                print(f"✅ Product {i+1}: {title[:60]}...")
                print(f"   💰 Price: {price or 'N/A'}")
                print(f"   🔗 URL: {link}")
                print()
                
            else:
                print(f"❌ Product {i+1}: Missing title or link")
                print(f"   Title: {title}")
                print(f"   Link: {link}")
                
        except Exception as e:
            print(f"⚠️ Error extracting product {i+1}: {e}")
            continue
    
    return results

def search_amazon_alternative(filters):
    """
    Dynamically constructs Amazon search query from filters.
    Skips fields with value 'any' and includes extra features if available.
    """
    driver = create_driver(headless=True)

    try:
        # Extract filters safely
        brand = filters.get('brand', '')
        color = filters.get('color', '')
        category = filters.get('category', '')
        gender = filters.get('gender', '')
        price = filters.get('price', '')
        other_features = filters.get('other_features', '')  # new field e.g., '7kg', 'for kids'

        # Only add if they are meaningful (not 'any' or empty)
        parts = []
        for value in [brand, color, category, gender]:
            if value and value != 'any':
                parts.append(value)

        # Add price constraint as phrase
        if price and price != 'any':
            parts.append(f"under {price}")

        # Add additional user-defined features like "7kg", "4-star", etc.
        if other_features and other_features != 'any':
            parts.append(other_features)

        refined_query = " ".join(parts).strip()
        
        search_url = f"https://www.amazon.in/s?k={quote_plus(refined_query)}"
        print(f"🔍 Navigating to: {search_url}")
        driver.get(search_url)
        time.sleep(2)

        return extract_product_results(driver)

    finally:
        driver.quit()



# Updated main search function
def search_amazon(filters):
    print(f"🔍 Starting Amazon search with filters: {filters}")
    try:
        print("🔄 Trying search method...")
        results = search_amazon_alternative(filters)
        
        # ✅ Filter by price if specified
        max_price = filters.get("price")
        if max_price:
            try:
                max_price = int(max_price)
                print(f"🔎 Filtering products under ₹{max_price}...")
                filtered = []
                for r in results:
                    try:
                        if r["price"]:
                            price_int = int("".join(filter(str.isdigit, r["price"])))
                            if price_int <= max_price:
                                filtered.append(r)
                    except:
                        continue
                results = filtered[:15]  # ✅ Limit to top 15 filtered
            except Exception as e:
                print("⚠️ Price filter parsing error:", e)

        return results or []
    except Exception as e:
        print(f"⚠️ Alternative search method failed: {e}")
        return []



def login_amazon(driver):
    print("👉 Login to Amazon manually...")
    driver.get("https://www.amazon.in/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.in%2F%3Fref_%3Dnav_ya_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=inflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0")
    time.sleep(5)

def add_to_cart_amazon(urls: list, *args, **kwargs):
    """
    Adds products to the Amazon cart after manual login.
    Accepts extra args for compatibility with agent frameworks like CrewAI.
    """
    if isinstance(urls, dict) and "urls" in urls:
        urls = urls["urls"]
    elif not isinstance(urls, list):
        raise ValueError("Expected a list of URLs or {'urls': [...]}, got: " + str(type(urls)))
    driver = create_driver(headless=False)

    # Manual login
    login_amazon(driver)
    input("🔐 After logging in, press ENTER to continue...")

    results = []

    for url in urls[:3]:
        try:
            driver.get(url)
            time.sleep(3)

            added = False

            try:
                add_button = driver.find_element(By.ID, "add-to-cart-button")
                driver.execute_script("arguments[0].click();", add_button)
                added = True
            except:
                pass

            if not added:
                try:
                    add_button = driver.find_element(By.XPATH, "//input[@value='Add to Cart' or @aria-label='Add to Cart']")
                    driver.execute_script("arguments[0].click();", add_button)
                    added = True
                except:
                    pass

            if added:
                print("✅ Added to cart:", url)
                results.append({"status": "added", "url": url})
            else:
                print("❌ Could not add to cart:", url)
                results.append({"status": "failed", "url": url, "error": "Button not found"})

            time.sleep(2)

        except Exception as e:
            print("❌ Error on product:", url, "|", e)
            results.append({"status": "failed", "url": url, "error": str(e)})

    print("🛒 Opening cart for verification...")
    driver.get("https://www.amazon.in/gp/cart/view.html")
    input("👀 Check the cart in the browser. Press ENTER to close the browser...")

    driver.quit()
    return results




# # Main function to be called by external search tool
def main(test_filters):
    results = search_amazon(test_filters)
    print(f"\n📋 Found {len(results)} results:")
    
    return results