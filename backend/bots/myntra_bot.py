# backend/bots/myntra_bot.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from urllib.parse import quote_plus

def search_myntra(filters):
    options = Options()
    options.add_argument("--headless=false")
    driver = webdriver.Chrome(options=options)

    # login_myntra(driver)

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
            time.sleep(3)
            title = driver.title
            results.append({"title": title, "url": link})
            # add_to_cart_myntra(driver, link)
        except Exception as e:
            print("❌ Error:", e)
            continue

    driver.quit()
    return results

def login_myntra(driver):
    print("👉 Login to Myntra manually in opened browser if required...")
    driver.get("https://www.myntra.com/login")
    time.sleep(15)

def add_to_cart_myntra(driver, product_url):
    driver.get(product_url)
    time.sleep(3)
    try:
        size_btn = driver.find_element(By.XPATH, "//p[text()='SELECT SIZE']/following::div[@class='size-buttons-buttonContainer']//button")
        size_btn.click()
        time.sleep(1)
        add_button = driver.find_element(By.XPATH, "//div[text()='ADD TO BAG']")
        add_button.click()
        print("✅ Added to cart:", product_url)
        time.sleep(2)
    except Exception as e:
        print("❌ Could not add to cart:", e)
