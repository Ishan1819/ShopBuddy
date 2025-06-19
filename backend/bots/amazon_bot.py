# # from selenium import webdriver
# # from selenium.webdriver.common.by import By
# # from selenium.webdriver.chrome.options import Options
# # from selenium.webdriver.support.ui import WebDriverWait
# # from selenium.webdriver.support import expected_conditions as EC
# # import time
# # from urllib.parse import quote_plus

# # def create_driver(headless=True):
# #     options = Options()
# #     options.add_argument("--headless=new" if headless else "--headless=false")
# #     options.add_argument("--no-sandbox")
# #     options.add_argument("--disable-dev-shm-usage")
# #     options.add_argument("--disable-blink-features=AutomationControlled")
# #     options.add_experimental_option("excludeSwitches", ["enable-automation"])
# #     options.add_experimental_option('useAutomationExtension', False)
# #     return webdriver.Chrome(options=options)

# # def search_amazon_improved(filters):
# #     """
# #     Improved Amazon search with better query construction and filtering
# #     """
# #     options = Options()
# #     options.add_argument("--headless=false")
# #     options.add_argument("--disable-blink-features=AutomationControlled")
# #     options.add_experimental_option("excludeSwitches", ["enable-automation"])
    
# #     driver = webdriver.Chrome(options=options)
# #     wait = WebDriverWait(driver, 10)
    
# #     try:
# #         # Method 1: Construct better search query
# #         # Put brand first, then category, then specifications
# #         query_parts = []
        
# #         if filters.get('brand'):
# #             query_parts.append(filters['brand'])
# #         if filters.get('category'):
# #             query_parts.append(filters['category'])
# #         if filters.get('gender'):
# #             query_parts.append(f"for {filters['gender']}")
# #         if filters.get('color'):
# #             query_parts.append(filters['color'])
            
# #         query = " ".join(query_parts)
# #         print(f"🔍 Searching for: {query}")
        
# #         # Navigate to Amazon with search
# #         url = f"https://www.amazon.in/s?k={quote_plus(query)}"
# #         driver.get(url)
# #         time.sleep(3)
        
# #         # Method 2: Apply filters using Amazon's filter system
# #         try:
# #             # Apply brand filter if available
# #             if filters.get('brand'):
# #                 brand_filter = apply_brand_filter(driver, filters['brand'])
# #                 if brand_filter:
# #                     time.sleep(2)
                    
# #             # Apply category filter
# #             if filters.get('category'):
# #                 category_filter = apply_category_filter(driver, filters['category'])
# #                 if category_filter:
# #                     time.sleep(2)
                    
# #         except Exception as e:
# #             print(f"⚠️ Filter application issue: {e}")
        
# #         # Apply price filter if provided
# #         try:
# #             if filters.get('min_price', 0) > 0 or filters.get('max_price', 999999) < 999999:
# #                 apply_price_filter(driver, filters.get('min_price', 0), filters.get('max_price', 999999))
# #                 time.sleep(3)
# #         except Exception as e:
# #             print("⚠️ Price filter issue:", e)
        
# #         # Extract results
# #         results = extract_product_results(driver)
# #         return results
        
# #     finally:
# #         # driver.quit()
# #         return results

# # def apply_brand_filter(driver, brand):
# #     """Apply brand filter on Amazon search results"""
# #     try:
# #         # Look for brand filter section
# #         brand_selectors = [
# #             f"//span[contains(text(), '{brand}')]/preceding-sibling::input[@type='checkbox']",
# #             f"//label[contains(text(), '{brand}')]/input[@type='checkbox']",
# #             f"//span[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{brand.lower()}')]/preceding-sibling::input[@type='checkbox']"
# #         ]
        
# #         for selector in brand_selectors:
# #             try:
# #                 brand_checkbox = driver.find_element(By.XPATH, selector)
# #                 if not brand_checkbox.is_selected():
# #                     driver.execute_script("arguments[0].click();", brand_checkbox)
# #                     print(f"✅ Applied {brand} brand filter")
# #                     return True
# #             except:
# #                 continue
                
# #         print(f"⚠️ Could not find {brand} brand filter")
# #         return False
        
# #     except Exception as e:
# #         print(f"❌ Brand filter error: {e}")
# #         return False

# # def apply_category_filter(driver, category):
# #     """Apply category filter on Amazon search results"""
# #     try:
# #         # Look for category filter in left sidebar
# #         category_selectors = [
# #             f"//span[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{category.lower()}')]/ancestor::a",
# #             f"//a[contains(@href, '{category.lower()}')]"
# #         ]
        
# #         for selector in category_selectors:
# #             try:
# #                 category_link = driver.find_element(By.XPATH, selector)
# #                 category_link.click()
# #                 print(f"✅ Applied {category} category filter")
# #                 return True
# #             except:
# #                 continue
                
# #         print(f"⚠️ Could not find {category} category filter")
# #         return False
        
# #     except Exception as e:
# #         print(f"❌ Category filter error: {e}")
# #         return False

# # def apply_price_filter(driver, min_price, max_price):
# #     """Apply price filter"""
# #     try:
# #         min_input = driver.find_element(By.ID, "low-price")
# #         max_input = driver.find_element(By.ID, "high-price")
        
# #         min_input.clear()
# #         max_input.clear()
        
# #         if min_price > 0:
# #             min_input.send_keys(str(min_price))
# #         if max_price < 999999:
# #             max_input.send_keys(str(max_price))
            
# #         # Find and click Go button
# #         go_button = driver.find_element(By.XPATH, "//input[@aria-labelledby='a-autoid-1-announce'] | //span[contains(text(), 'Go')]/parent::span/parent::button")
# #         go_button.click()
# #         print(f"✅ Applied price filter: ₹{min_price} - ₹{max_price}")
        
# #     except Exception as e:
# #         print(f"❌ Price filter error: {e}")
# #         raise e

# # def extract_product_results(driver):
# #     """Extract product information from search results"""
# #     results = []
    
# #     # Multiple selectors for product containers
# #     product_selectors = [
# #         "//div[@data-component-type='s-search-result']",
# #         "//div[contains(@class, 's-result-item')]",
# #         "//div[@data-asin and @data-asin!='']"
# #     ]
    
# #     products = []
# #     for selector in product_selectors:
# #         try:
# #             products = driver.find_elements(By.XPATH, selector)
# #             if products:
# #                 break
# #         except:
# #             continue
    
# #     print(f"📦 Found {len(products)} products")
    
# #     for i, product in enumerate(products[:15]):  # Get more results
# #         try:
# #             # Extract title with more comprehensive selectors
# #             title_selectors = [
# #                 ".//h2//span[contains(@class, 'a-size-mini')]",
# #                 ".//h2//span[contains(@class, 'a-size-base-plus')]",
# #                 ".//h2//a//span",
# #                 ".//h2//span",
# #                 ".//a[contains(@class, 's-link-style')]//span",
# #                 ".//span[contains(@class, 's-size-mini')]"
# #             ]
            
# #             title = None
# #             for title_sel in title_selectors:
# #                 try:
# #                     title_elem = product.find_element(By.XPATH, title_sel)
# #                     title = title_elem.text.strip()
# #                     if title and len(title) > 10:  # Ensure we get meaningful title
# #                         break
# #                 except:
# #                     continue
            
# #             # Extract link with better error handling
# #             link_selectors = [
# #                 ".//h2//a[@href]",
# #                 ".//a[contains(@class, 's-link-style')][@href]",
# #                 ".//a[@href and contains(@href, '/dp/')]"
# #             ]
            
# #             link = None
# #             for link_sel in link_selectors:
# #                 try:
# #                     link_elem = product.find_element(By.XPATH, link_sel)
# #                     raw_link = link_elem.get_attribute("href")
# #                     if raw_link:
# #                         # Clean and validate URL
# #                         if raw_link.startswith("http"):
# #                             link = raw_link
# #                         elif raw_link.startswith("/"):
# #                             link = f"https://www.amazon.in{raw_link}"
# #                         else:
# #                             link = f"https://www.amazon.in/{raw_link}"
                        
# #                         # Validate that it's a product URL
# #                         if "/dp/" in link or "/gp/product/" in link:
# #                             break
# #                         else:
# #                             link = None
# #                 except Exception as e:
# #                     print(f"🔗 Link extraction error for selector {link_sel}: {e}")
# #                     continue
            
# #             # Extract price with better handling
# #             price_selectors = [
# #                 ".//span[@class='a-price-whole']",
# #                 ".//span[contains(@class, 'a-price-whole')]",
# #                 ".//span[@class='a-offscreen']",
# #                 ".//span[contains(@class, 'a-price')]//span[@aria-hidden='true']"
# #             ]
            
# #             price = None
# #             for price_sel in price_selectors:
# #                 try:
# #                     price_elem = product.find_element(By.XPATH, price_sel)
# #                     price_text = price_elem.get_attribute("textContent") or price_elem.text
# #                     if price_text and any(char.isdigit() for char in price_text):
# #                         price = price_text.strip().replace(',', '')
# #                         break
# #                 except:
# #                     continue
            
# #             # Additional validation and debugging
# #             if title and link:
# #                 # Validate URL format
# #                 if not any(pattern in link for pattern in ["/dp/", "/gp/product/", "amazon.in"]):
# #                     print(f"⚠️ Suspicious URL format: {link}")
# #                     continue
                
# #                 # Clean up title
# #                 title = title.replace('\n', ' ').strip()
                
# #                 result = {
# #                     "title": title,
# #                     "url": link,
# #                     "price": price,
# #                     "position": i + 1
# #                 }
                
# #                 results.append(result)
# #                 print(f"✅ Product {i+1}: {title[:60]}...")
# #                 print(f"   💰 Price: {price or 'N/A'}")
# #                 print(f"   🔗 URL: {link}")
# #                 print()
                
# #             else:
# #                 print(f"❌ Product {i+1}: Missing title or link")
# #                 print(f"   Title: {title}")
# #                 print(f"   Link: {link}")
                
# #         except Exception as e:
# #             print(f"⚠️ Error extracting product {i+1}: {e}")
# #             continue
    
# #     return results

# # def search_amazon_alternative(filters):
# #     """
# #     Alternative approach using direct category URLs
# #     """
# #     driver = create_driver(headless=False)
    
# #     try:
# #         # Start with category-specific URL
# #         category_urls = {
# #             "shoes": "https://www.amazon.in/s?i=shoes&ref=nb_sb_noss",
# #             "running shoes": "https://www.amazon.in/s?k=running+shoes&i=fashion&ref=nb_sb_noss",
# #             "sneakers": "https://www.amazon.in/s?k=sneakers&i=fashion&ref=nb_sb_noss"
# #         }
        
# #         base_url = category_urls.get(filters.get('category', '').lower(), 
# #                                 "https://www.amazon.in/s?k=" + quote_plus(filters.get('category', 'shoes')))
        
# #         driver.get(base_url)
# #         time.sleep(3)
        
# #         # Then apply additional filters
# #         search_box = driver.find_element(By.ID, "twotabsearchtextbox")
# #         search_box.clear()
        
# #         # Construct refined search
# #         refined_query = f"{filters.get('brand', '')} {filters.get('color', '')} {filters.get('category', '')} {filters.get('gender', '')}"
# #         search_box.send_keys(refined_query.strip())
# #         search_box.submit()
        
# #         time.sleep(3)
        
# #         return extract_product_results(driver)
        
# #     finally:
# #         return extract_product_results(driver)

# # # Updated main search function
# # def search_amazon(filters):
# #     """Main search function with fallback methods"""
# #     print(f"🔍 Starting Amazon search with filters: {filters}")
    
# #     # Try improved method first
# #     try:
# #         results = search_amazon_improved(filters)
# #         if results:
# #             return results
# #     except Exception as e:
# #         print(f"⚠️ Primary search method failed: {e}")
    
# #     # Fallback to alternative method
# #     try:
# #         print("🔄 Trying alternative search method...")
# #         results = search_amazon_alternative(filters)
# #         if results:
# #             return results
# #     except Exception as e:
# #         print(f"⚠️ Alternative search method failed: {e}")
    
# #     # Return empty if all methods fail
# #     return []

# # # Rest of your existing functions remain the same
# # def login_amazon(driver):
# #     print("👉 Login to Amazon manually...")
# #     driver.get("https://www.amazon.in/ap/signin")
# #     time.sleep(20)

# # def add_to_cart_amazon(urls: list):
# #     driver = create_driver(headless=False)
    
# #     # Optional: Login manually if needed
# #     login_amazon(driver)
    
# #     results = []
# #     for url in urls[:3]:
# #         try:
# #             driver.get(url)
# #             time.sleep(3)
            
# #             # Multiple selectors for add to cart button
# #             cart_selectors = [
# #                 "add-to-cart-button",
# #                 "cart",
# #                 "a-button-input"
# #             ]
            
# #             added = False
# #             for selector in cart_selectors:
# #                 try:
# #                     add_button = driver.find_element(By.ID, selector)
# #                     add_button.click()
# #                     print("✅ Added to cart:", url)
# #                     results.append({"status": "added", "url": url})
# #                     added = True
# #                     break
# #                 except:
# #                     continue
            
# #             if not added:
# #                 # Try by text
# #                 try:
# #                     add_button = driver.find_element(By.XPATH, "//span[contains(text(), 'Add to Cart')]/parent::button")
# #                     add_button.click()
# #                     print("✅ Added to cart:", url)
# #                     results.append({"status": "added", "url": url})
# #                 except Exception as e:
# #                     print("❌ Could not add to cart:", url, "| Error:", e)
# #                     results.append({"status": "failed", "url": url, "error": str(e)})
            
# #             time.sleep(2)
            
# #         except Exception as e:
# #             print("❌ Could not add to cart:", url, "| Error:", e)
# #             results.append({"status": "failed", "url": url, "error": str(e)})
    
# #     # driver.quit()
# #     return results

# # # Example usage
# # # if __name__ == "__main__":
# # #     # Test the improved search
# # #     test_filters = {
# # #         'material': 'any',
# # #         'brand': 'Nike',
# # #         'color': 'white',
# # #         'category': 'running shoes',
# # #         'gender': 'men',
# # #         'min_price': 2000,
# # #         'max_price': 8000,
# # #         'min_rating': 4.0
# # #     }
# # #     # print(test_filters)
# # #     # print(type(test_filters))
# # #     results = search_amazon(test_filters)
# # #     print(f"\n📋 Found {len(results)} results:")
# # #     for i, result in enumerate(results, 1):
# # #         print(f"{i}. {result['title']}")
# # #         print(f"   Price: {result.get('price', 'N/A')}")
# # #         print(f"   URL: {result['url'][:80]}...")
# # #         print()


# # # -------------------------------------------------------------------------------------

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
    Alternative approach using dynamic search URL
    """
    driver = create_driver(headless=False)

    try:
        # Construct refined search
        refined_query = f"{filters.get('brand', '')} {filters.get('color', '')} {filters.get('category', '')} {filters.get('gender', '')}".strip()
        search_url = f"https://www.amazon.in/s?k={quote_plus(refined_query)}"
        
        print(f"🔍 Navigating to: {search_url}")
        driver.get(search_url)
        time.sleep(2)

        return extract_product_results(driver)
        
    finally:
        driver.quit()


# Updated main search function
def search_amazon(filters):
    """Main search function with fallback methods"""
    print(f"🔍 Starting Amazon search with filters: {filters}")
    
    try:
        print("🔄 Trying search method...")
        results = search_amazon_alternative(filters)
        if results:
            return results
    except Exception as e:
        print(f"⚠️ Alternative search method failed: {e}")
    
    # Return empty if all methods fail
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
    # for i, result in enumerate(results, 1):
    #     print(f"{i}. {result['title']}")
    #     print(f"   Price: {result.get('price', 'N/A')}")
    #     print(f"   URL: {result['url'][:700]}...")
    #     print()
    
    return results





