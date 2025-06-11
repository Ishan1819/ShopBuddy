# backend/bots/flipkart_bot.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from urllib.parse import quote_plus

def search_flipkart(filters):
    options = Options()
    options.add_argument("--headless=false")
    driver = webdriver.Chrome(options=options)

    # login_flipkart(driver)

    query = f"{filters['brand']} {filters['color']} {filters['category']}"
    url = f"https://www.flipkart.com/search?q={quote_plus(query)}"
    driver.get(url)
    time.sleep(3)

    results = []
    products = driver.find_elements(By.XPATH, "//a[contains(@href,'/p/')]")
    for product in products[:10]:
        try:
            link = product.get_attribute("href")
            driver.get(link)
            time.sleep(3)
            title = driver.title
            results.append({"title": title, "url": link})
            # add_to_cart_flipkart(driver, link)
        except Exception as e:
            print("❌ Error:", e)
            continue

    driver.quit()
    return results

def login_flipkart(driver):
    print("👉 Login to Flipkart manually in opened browser if required...")
    driver.get("https://www.flipkart.com/account/login")
    time.sleep(15)

def add_to_cart_flipkart(driver, product_url):
    driver.get(product_url)
    time.sleep(3)
    try:
        add_button = driver.find_element(By.XPATH, "//button[contains(text(),'Add to cart')]")
        add_button.click()
        print("✅ Added to cart:", product_url)
        time.sleep(2)
    except Exception as e:
        print("❌ Could not add to cart:", e)
