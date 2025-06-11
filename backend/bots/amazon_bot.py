# backend/bots/amazon_bot.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from urllib.parse import quote_plus

def search_amazon(filters):
    options = Options()
    options.add_argument("--headless=false")  # Use visible browser
    driver = webdriver.Chrome(options=options)

    # 👉 Optional: Login placeholder
    # login_amazon(driver)

    query = f"{filters['brand']} {filters['color']} {filters['category']}"
    url = f"https://www.amazon.in/s?k={quote_plus(query)}"
    driver.get(url)
    time.sleep(3)

    # 👉 Apply price filters
    try:
        if filters['min_price'] > 0 or filters['max_price'] < 999999:
            min_input = driver.find_element(By.ID, "low-price")
            max_input = driver.find_element(By.ID, "high-price")
            min_input.send_keys(str(filters['min_price']))
            max_input.send_keys(str(filters['max_price']))
            go_button = driver.find_element(By.XPATH, "//input[@aria-labelledby='a-autoid-1-announce']")
            go_button.click()
            time.sleep(3)
    except Exception as e:
        print("Price filter failed:", e)

    results = []
    products = driver.find_elements(By.XPATH, "//div[@data-component-type='s-search-result']")
    for product in products[:10]:
        try:
            title = product.find_element(By.TAG_NAME, "h2").text
            link = product.find_element(By.TAG_NAME, "a").get_attribute("href")
            full_link = link
            results.append({"title": title, "url": full_link})
            # add_to_cart_amazon(driver, full_link)
        except Exception:
            continue

    driver.quit()
    return results

def login_amazon(driver):
    print("👉 Login to Amazon manually in opened browser if required...")
    driver.get("https://www.amazon.in/ap/signin")
    time.sleep(15)  # Allow time for manual login

def add_to_cart_amazon(driver, product_url):
    driver.get(product_url)
    # time.sleep(3)
    try:
        add_button = driver.find_element(By.ID, "add-to-cart-button")
        add_button.click()
        print("✅ Added to cart:", product_url)
        time.sleep(2)
    except Exception as e:
        print("❌ Could not add to cart:", e)
