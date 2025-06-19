from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from urllib.parse import quote_plus

def create_driver(headless=True):
    options = Options()
    options.add_argument("--headless=new" if headless else "--headless=false")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=options)

def search_myntra(filters):
    driver = create_driver()
    query = f"{filters['brand']} {filters['color']} {filters['category']}"
    url = f"https://www.myntra.com/{quote_plus(query)}"
    driver.get(url)
    time.sleep(3)

    results = []
    products = driver.find_elements(By.XPATH, "//li[@class='product-base']/a")
    for product in products[:10]:
        try:
            link = product.get_attribute("href")
            driver.get(link)
            time.sleep(2)
            title = driver.title
            results.append({"title": title, "url": link})
        except Exception as e:
            print("❌ Error extracting product:", e)
            continue

    driver.quit()
    return results

def add_to_cart_myntra(urls: list):
    driver = create_driver(headless=False)  # Headless must be False for interaction

    # Optional: login manually
    login_myntra(driver)

    results = []
    for url in urls[:3]:
        try:
            driver.get(url)
            time.sleep(3)
            
            # Select available size
            size_btn = driver.find_element(By.XPATH, "//p[text()='SELECT SIZE']/following::div[@class='size-buttons-buttonContainer']//button")
            size_btn.click()
            time.sleep(1)

            # Click 'Add to Bag'
            add_button = driver.find_element(By.XPATH, "//div[text()='ADD TO BAG']")
            add_button.click()
            print("✅ Added to cart:", url)
            results.append({"status": "added", "url": url})
            time.sleep(2)

        except Exception as e:
            print("❌ Failed to add to cart:", e)
            results.append({"status": "failed", "url": url, "error": str(e)})
            continue

    driver.quit()
    return results

def login_myntra(driver):
    print("👉 Please login manually in the opened browser...")
    driver.get("https://www.myntra.com/login")
    time.sleep(20)  # Give user time to log in manually
