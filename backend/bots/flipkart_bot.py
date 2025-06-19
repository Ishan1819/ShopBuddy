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

def search_flipkart(filters):
    driver = create_driver()
    query = f"{filters['brand']} {filters['color']} {filters['category']}"
    url = f"https://www.flipkart.com/search?q={quote_plus(query)}"
    driver.get(url)
    time.sleep(3)

    results = []
    products = driver.find_elements(By.XPATH, "//a[contains(@href,'/p/')]")
    seen = set()

    for product in products:
        try:
            link = product.get_attribute("href")
            if link in seen:
                continue
            seen.add(link)
            driver.get(link)
            time.sleep(2)
            title = driver.title
            results.append({"title": title, "url": link})
            if len(results) >= 10:
                break
        except Exception as e:
            print("❌ Error:", e)
            continue

    driver.quit()
    return results

def login_flipkart(driver):
    print("👉 Login to Flipkart manually...")
    driver.get("https://www.flipkart.com/account/login")
    time.sleep(20)

def add_to_cart_flipkart(urls: list):
    driver = create_driver(headless=False)

    # Optional manual login if needed
    login_flipkart(driver)

    results = []
    for url in urls[:3]:
        try:
            driver.get(url)
            time.sleep(3)
            add_button = driver.find_element(By.XPATH, "//button[contains(text(),'Add to cart')]")
            add_button.click()
            print("✅ Added to cart:", url)
            results.append({"status": "added", "url": url})
            time.sleep(2)
        except Exception as e:
            print("❌ Could not add to cart:", url, "| Error:", e)
            results.append({"status": "failed", "url": url, "error": str(e)})

    driver.quit()
    return results
