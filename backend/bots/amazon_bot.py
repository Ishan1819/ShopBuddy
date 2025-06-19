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

def create_driver(headless=True):
    options = Options()
    options.add_argument("--headless=new" if headless else "--headless=false")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    return webdriver.Chrome(options=options)

def search_amazon_improved(filters):
    """
    Improved Amazon search with better query construction and filtering
    """
    options = Options()
    options.add_argument("--headless=false")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)
    
    try:
        # Method 1: Construct better search query
        # Put brand first, then category, then specifications
        query_parts = []
        
        if filters.get('brand'):
            query_parts.append(filters['brand'])
        if filters.get('category'):
            query_parts.append(filters['category'])
        if filters.get('gender'):
            query_parts.append(f"for {filters['gender']}")
        if filters.get('color'):
            query_parts.append(filters['color'])
            
        query = " ".join(query_parts)
        print(f"🔍 Searching for: {query}")
        
        # Navigate to Amazon with search
        url = f"https://www.amazon.in/s?k={quote_plus(query)}"
        driver.get(url)
        time.sleep(5)
        
        # Method 2: Apply filters using Amazon's filter system
        try:
            # Apply brand filter if available
            if filters.get('brand'):
                brand_filter = apply_brand_filter(driver, filters['brand'])
                if brand_filter:
                    time.sleep(5)

            # Apply category filter
            if filters.get('category'):
                category_filter = apply_category_filter(driver, filters['category'])
                if category_filter:
                    time.sleep(5)

        except Exception as e:
            print(f"⚠️ Filter application issue: {e}")
        
        # Apply price filter if provided
        try:
            if filters.get('min_price', 0) > 0 or filters.get('max_price', 999999) < 999999:
                apply_price_filter(driver, filters.get('min_price', 0), filters.get('max_price', 999999))
                time.sleep(5)
        except Exception as e:
            print("⚠️ Price filter issue:", e)
        
        # Extract results
        results = extract_product_results(driver)
        return results
        
    finally:
        driver.quit()

def apply_brand_filter(driver, brand):
    """Apply brand filter on Amazon search results"""
    try:
        # Look for brand filter section
        brand_selectors = [
            f"//span[contains(text(), '{brand}')]/preceding-sibling::input[@type='checkbox']",
            f"//label[contains(text(), '{brand}')]/input[@type='checkbox']",
            f"//span[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{brand.lower()}')]/preceding-sibling::input[@type='checkbox']"
        ]
        
        for selector in brand_selectors:
            try:
                brand_checkbox = driver.find_element(By.XPATH, selector)
                if not brand_checkbox.is_selected():
                    driver.execute_script("arguments[0].click();", brand_checkbox)
                    print(f"✅ Applied {brand} brand filter")
                    return True
            except:
                continue
                
        print(f"⚠️ Could not find {brand} brand filter")
        return False
        
    except Exception as e:
        print(f"❌ Brand filter error: {e}")
        return False

def apply_category_filter(driver, category):
    """Apply category filter on Amazon search results"""
    try:
        # Look for category filter in left sidebar
        category_selectors = [
            f"//span[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{category.lower()}')]/ancestor::a",
            f"//a[contains(@href, '{category.lower()}')]"
        ]
        
        for selector in category_selectors:
            try:
                category_link = driver.find_element(By.XPATH, selector)
                category_link.click()
                print(f"✅ Applied {category} category filter")
                return True
            except:
                continue
                
        print(f"⚠️ Could not find {category} category filter")
        return False
        
    except Exception as e:
        print(f"❌ Category filter error: {e}")
        return False

def apply_price_filter(driver, min_price, max_price):
    """Apply price filter"""
    try:
        min_input = driver.find_element(By.ID, "low-price")
        max_input = driver.find_element(By.ID, "high-price")
        
        min_input.clear()
        max_input.clear()
        
        if min_price > 0:
            min_input.send_keys(str(min_price))
        if max_price < 999999:
            max_input.send_keys(str(max_price))
            
        # Find and click Go button
        go_button = driver.find_element(By.XPATH, "//input[@aria-labelledby='a-autoid-1-announce'] | //span[contains(text(), 'Go')]/parent::span/parent::button")
        go_button.click()
        print(f"✅ Applied price filter: ₹{min_price} - ₹{max_price}")
        
    except Exception as e:
        print(f"❌ Price filter error: {e}")
        raise e

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
    Alternative approach using direct category URLs
    """
    driver = create_driver(headless=False)
    
    try:
        # Start with category-specific URL
        category_urls = {
            "shoes": "https://www.amazon.in/s?i=shoes&ref=nb_sb_noss",
            "running shoes": "https://www.amazon.in/s?k=running+shoes&i=fashion&ref=nb_sb_noss",
            "sneakers": "https://www.amazon.in/s?k=sneakers&i=fashion&ref=nb_sb_noss"
        }
        
        base_url = category_urls.get(filters.get('category', '').lower(), 
                                "https://www.amazon.in/s?k=" + quote_plus(filters.get('category', 'shoes')))
        
        driver.get(base_url)
        time.sleep(5)
        
        # Then apply additional filters
        search_box = driver.find_element(By.ID, "twotabsearchtextbox")
        search_box.clear()
        
        # Construct refined search
        refined_query = f"{filters.get('brand', '')} {filters.get('color', '')} {filters.get('category', '')} {filters.get('gender', '')}"
        search_box.send_keys(refined_query.strip())
        search_box.submit()

        time.sleep(5)

        return extract_product_results(driver)
        
    finally:
        driver.quit()

# Updated main search function
def search_amazon(filters):
    """Main search function with fallback methods"""
    print(f"🔍 Starting Amazon search with filters: {filters}")
    
    # Try improved method first
    try:
        results = search_amazon_improved(filters)
        if results:
            return results
    except Exception as e:
        print(f"⚠️ Primary search method failed: {e}")
    
    # Fallback to alternative method
    try:
        print("🔄 Trying alternative search method...")
        results = search_amazon_alternative(filters)
        if results:
            return results
    except Exception as e:
        print(f"⚠️ Alternative search method failed: {e}")
    
    # Return empty if all methods fail
    return []

def login_amazon(driver):
    print("👉 Login to Amazon manually...")
    driver.get("https://www.amazon.in/ap/signin")
    time.sleep(5)

def add_to_cart_amazon(urls: list):
    driver = create_driver(headless=False)
    
    # Optional: Login manually if needed
    login_amazon(driver)
    
    results = []
    for url in urls[:3]:
        try:
            driver.get(url)
            time.sleep(5)
            
            # Multiple selectors for add to cart button
            cart_selectors = [
                "add-to-cart-button",
                "cart",
                "a-button-input"
            ]
            
            added = False
            for selector in cart_selectors:
                try:
                    add_button = driver.find_element(By.ID, selector)
                    add_button.click()
                    print("✅ Added to cart:", url)
                    results.append({"status": "added", "url": url})
                    added = True
                    break
                except:
                    continue
            
            if not added:
                # Try by text
                try:
                    add_button = driver.find_element(By.XPATH, "//span[contains(text(), 'Add to Cart')]/parent::button")
                    add_button.click()
                    print("✅ Added to cart:", url)
                    results.append({"status": "added", "url": url})
                except Exception as e:
                    print("❌ Could not add to cart:", url, "| Error:", e)
                    results.append({"status": "failed", "url": url, "error": str(e)})
            
            time.sleep(5)
            
        except Exception as e:
            print("❌ Could not add to cart:", url, "| Error:", e)
            results.append({"status": "failed", "url": url, "error": str(e)})
    
    driver.quit()
    return results

# # Main function to be called by external search tool
def main(test_filters):
    results = search_amazon(test_filters)
    print(f"\n📋 Found {len(results)} results:")
    for i, result in enumerate(results, 1):
        print(f"{i}. {result['title']}")
        print(f"   Price: {result.get('price', 'N/A')}")
        print(f"   URL: {result['url'][:80]}...")
        print()
    
    return results





# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# import time

# def main(filters):
#     query = f"{filters.get('brand', '')} {filters.get('gender', '')} {filters.get('category', '')} {filters.get('color', '')}"
#     query = query.replace("  ", " ").strip()

#     print(f"🛒 Searching Amazon for: {query}")

#     options = Options()
#     options.add_argument("--start-maximized")
#     driver = webdriver.Chrome(options=options)

#     # Go to Amazon and search
#     driver.get(f"https://www.amazon.in/s?k={query.replace(' ', '+')}")
#     time.sleep(5)

#     # Accept cookies or dismiss modals if needed (optional)
    
#     product_links = []
#     try:
#         # Target actual product containers
#         products = driver.find_elements(By.XPATH, "//a[@class='a-link-normal s-no-outline']")
#         for product in products[:5]:  # You can increase or decrease this limit
#             link = product.get_attribute("href")
#             if link and "/dp/" in link:
#                 product_links.append(link)
#     except Exception as e:
#         print("Error during scraping:", e)
    
#     print("✅ Found product links:", product_links)
#     # Don't quit if you want to keep the window open for debugging
#     # driver.quit()

#     return product_links


# def add_to_cart_amazon(product_urls):
#     options = webdriver.ChromeOptions()
#     options.add_argument("--start-maximized")
#     driver = webdriver.Chrome(options=options)

#     for url in product_urls[:3]:
#         try:
#             driver.get(url)
#             time.sleep(3)

#             # Try to click the Add to Cart button
#             add_to_cart_button = driver.find_element(By.ID, "add-to-cart-button")
#             add_to_cart_button.click()

#             print(f"✅ Added to cart: {url}")
#             time.sleep(2)

#         except Exception as e:
#             print(f"❌ Failed to add to cart: {url} | Error: {e}")

#     input("🛒 Cart operation complete. Check browser and press Enter to close.")
#     driver.quit()

#     return {"status": "done", "message": "Top 3 products added to Amazon cart."}







# _______________________________________________________________________________________
# ________________________________________________________________________________________
# ________________________________________________________________________________________


# import time
# import re
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.chrome.options import Options
# from selenium.common.exceptions import TimeoutException, NoSuchElementException
# from urllib.parse import urlencode, quote_plus

# class AmazonProductSearcher:
#     def __init__(self, headless=True):
#         """
#         Initialize the Amazon searcher
        
#         Args:
#             headless (bool): Whether to run browser in headless mode
#         """
#         self.driver = None
#         self.headless = headless
        
#     def setup_driver(self):
#         """Setup Chrome driver with appropriate options"""
#         chrome_options = Options()
        
#         # Always run in headless mode
#         chrome_options.add_argument("--headless")
#         chrome_options.add_argument("--no-sandbox")
#         chrome_options.add_argument("--disable-dev-shm-usage")
#         chrome_options.add_argument("--disable-blink-features=AutomationControlled")
#         chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
#         chrome_options.add_experimental_option('useAutomationExtension', False)
        
#         # User agent to avoid detection
#         chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        
#         self.driver = webdriver.Chrome(options=chrome_options)
#         self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
#     def create_search_query(self, filter_dict):
#         """
#         Create search query from filter dictionary
        
#         Args:
#             filter_dict (dict): Dictionary containing filter criteria
            
#         Returns:
#             str: Formatted search query
#         """
#         query_parts = []
        
#         # Add brand if specified
#         if filter_dict.get('brand') and filter_dict['brand'].lower() != 'any':
#             query_parts.append(filter_dict['brand'])
            
#         # Add category
#         if filter_dict.get('category'):
#             query_parts.append(filter_dict['category'])
            
#         # Add gender
#         if filter_dict.get('gender') and filter_dict['gender'].lower() != 'any':
#             if filter_dict['gender'].lower() in ['men', 'women', 'boys', 'girls']:
#                 query_parts.append(f"for {filter_dict['gender']}")
#             else:
#                 query_parts.append(filter_dict['gender'])
                
#         # Add color
#         if filter_dict.get('color') and filter_dict['color'].lower() != 'any':
#             query_parts.append(f"{filter_dict['color']} color")
            
#         # Add price range
#         max_price = filter_dict.get('max_price')
#         if max_price and max_price > 0:
#             query_parts.append(f"under {max_price}")
            
#         return " ".join(query_parts)
    
#     def search_amazon(self, search_query):
#         """
#         Search Amazon with the given query
        
#         Args:
#             search_query (str): Search query string
            
#         Returns:
#             bool: True if search was successful
#         """
#         try:
#             # Go to Amazon
#             self.driver.get("https://www.amazon.com")
#             time.sleep(2)
            
#             # Find search box and enter query
#             search_box = WebDriverWait(self.driver, 10).until(
#                 EC.presence_of_element_located((By.ID, "twotabsearchtextbox"))
#             )
            
#             search_box.clear()
#             search_box.send_keys(search_query)
            
#             # Click search button
#             search_button = self.driver.find_element(By.ID, "nav-search-submit-button")
#             search_button.click()
            
#             # Wait for results to load
#             WebDriverWait(self.driver, 10).until(
#                 EC.presence_of_element_located((By.CSS_SELECTOR, "[data-component-type='s-search-result']"))
#             )
            
#             return True
            
#         except TimeoutException:
#             print("Timeout waiting for Amazon search results")
#             return False
#         except Exception as e:
#             print(f"Error during Amazon search: {str(e)}")
#             return False
    
#     def extract_product_urls(self, max_products=10):
#         """
#         Extract product URLs from search results
        
#         Args:
#             max_products (int): Maximum number of products to extract
            
#         Returns:
#             list: List of product URLs (never None)
#         """
#         product_urls = []
        
#         try:
#             # Wait a bit for page to fully load
#             time.sleep(3)
            
#             # Find all product containers with multiple selectors
#             product_containers = []
            
#             # Try different selectors for product containers
#             selectors = [
#                 "[data-component-type='s-search-result']",
#                 ".s-result-item",
#                 "[data-asin]:not([data-asin=''])"
#             ]
            
#             for selector in selectors:
#                 try:
#                     containers = self.driver.find_elements(By.CSS_SELECTOR, selector)
#                     if containers:
#                         product_containers = containers
#                         print(f"Found {len(containers)} products using selector: {selector}")
#                         break
#                 except:
#                     continue
            
#             if not product_containers:
#                 print("No product containers found with any selector")
#                 return []
            
#             for i, container in enumerate(product_containers[:max_products]):
#                 try:
#                     # Try multiple selectors for product links
#                     link_selectors = [
#                         "h2 a",
#                         ".s-link-style a",
#                         "a[href*='/dp/']",
#                         "a[href*='/gp/product/']",
#                         ".a-link-normal"
#                     ]
                    
#                     title_link = None
#                     for link_selector in link_selectors:
#                         try:
#                             title_link = container.find_element(By.CSS_SELECTOR, link_selector)
#                             if title_link:
#                                 break
#                         except:
#                             continue
                    
#                     if not title_link:
#                         continue
                    
#                     # Get the href attribute
#                     href = title_link.get_attribute('href')
                    
#                     if href and ('amazon.com' in href or href.startswith('/')):
#                         # Handle relative URLs
#                         if href.startswith('/'):
#                             href = f"https://www.amazon.com{href}"
                        
#                         # Keep the full URL with all search parameters
#                         # This preserves the search context and query parameters
#                         if '/dp/' in href or '/gp/product/' in href or 'amazon.com' in href:
#                             product_urls.append(href)
                            
#                 except Exception as e:
#                     print(f"Error extracting URL from product {i+1}: {str(e)}")
#                     continue
            
#             print(f"Successfully extracted {len(product_urls)} product URLs")
#             return product_urls
            
#         except Exception as e:
#             print(f"Error extracting product URLs: {str(e)}")
#             return []
    
#     def close_driver(self):
#         """Close the browser driver"""
#         if self.driver:
#             self.driver.quit()
    
#     def search_products(self, filter_dict, max_products=10):
#         """
#         Main function to search for products based on filter criteria
        
#         Args:
#             filter_dict (dict): Dictionary containing filter criteria
#             max_products (int): Maximum number of products to return
            
#         Returns:
#             dict: Dictionary containing search query and product URLs
#         """
#         try:
#             # Validate input
#             if not filter_dict or not isinstance(filter_dict, dict):
#                 return {"error": "Invalid filter dictionary provided", "product_urls": []}
            
#             # Setup driver
#             self.setup_driver()
            
#             # Create search query
#             search_query = self.create_search_query(filter_dict)
#             if not search_query.strip():
#                 return {"error": "Could not create search query from filters", "product_urls": []}
            
#             print(f"Search Query: {search_query}")
            
#             # Search Amazon
#             if not self.search_amazon(search_query):
#                 return {"error": "Failed to search Amazon", "product_urls": []}
            
#             # Extract product URLs
#             product_urls = self.extract_product_urls(max_products)
            
#             # Ensure we always return a list, even if empty
#             if product_urls is None:
#                 product_urls = []
            
#             result = {
#                 "search_query": search_query,
#                 "total_products_found": len(product_urls),
#                 "product_urls": product_urls,
#                 "status": "success" if product_urls else "no_products_found"
#             }
            
#             return result
            
#         except Exception as e:
#             error_msg = f"An error occurred: {str(e)}"
#             print(error_msg)
#             return {
#                 "error": error_msg,
#                 "product_urls": [],
#                 "search_query": "",
#                 "total_products_found": 0,
#                 "status": "error"
#             }
        
#         finally:
#             self.close_driver()

# def main(filter_dict):
#     """
#     Main function to demonstrate the Amazon product searcher
#     """
#     # Example filter dictionary
#     # filter_dict = {
#     #     'platform': ['amazon'], 
#     #     'category': 'shoes', 
#     #     'brand': 'Nike', 
#     #     'gender': 'men', 
#     #     'color': 'white', 
#     #     'material': 'any', 
#     #     'min_price': 0, 
#     #     'max_price': 6000, 
#     #     'min_rating': 4.0
#     # }
    
#     # Create searcher instance (runs in headless mode by default)
#     searcher = AmazonProductSearcher()
    
#     # Search for products
#     print("Starting Amazon product search (running in background)...")
#     results = searcher.search_products(filter_dict, max_products=10)
    
#     # Display results
#     if "error" in results:
#         print(f"Error: {results['error']}")
#         print(f"Status: {results.get('status', 'unknown')}")
#     else:
#         print(f"\nSearch Query: {results['search_query']}")
#         print(f"Status: {results['status']}")
#         print(f"Total Products Found: {results['total_products_found']}")
        
#         if results['product_urls']:
#             print("\nProduct URLs:")
#             for i, url in enumerate(results['product_urls'], 1):
#                 print(f"{i}. {url}")
#         else:
#             print("\nNo product URLs found. This could be due to:")
#             print("- Amazon blocking automated requests")
#             print("- Search returned no results")
#             print("- Page structure changes")
    
#     print("\nSearch completed!")

# # if __name__ == "__main__":
# #     main()