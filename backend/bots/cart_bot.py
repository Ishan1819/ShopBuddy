# backend/bots/cart_bot.py

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

from backend.bots.amazon_bot import add_to_cart_amazon
from backend.bots.flipkart_bot import add_to_cart_flipkart
from backend.bots.myntra_bot import add_to_cart_myntra

def add_to_cart(product_list):
    options = Options()
    options.add_argument("--headless=false")
    driver = webdriver.Chrome(options=options)

    # 🔧 Fix starts here
    if isinstance(product_list, str):
        product_list = [{"url": product_list}]
    elif isinstance(product_list, dict):
        product_list = [product_list]
    elif isinstance(product_list, list) and all(isinstance(item, str) for item in product_list):
        product_list = [{"url": u} for u in product_list]
    # 🔧 Fix ends here

    for product in product_list:
        url = product.get("url", "")
        if "amazon" in url:
            try:
                add_to_cart_amazon([url])
            except Exception as e:
                print("❌ Amazon cart error:", e)

        elif "flipkart" in url:
            try:
                add_to_cart_flipkart(driver, url)
            except Exception as e:
                print("❌ Flipkart cart error:", e)

        elif "myntra" in url:
            try:
                add_to_cart_myntra(driver, url)
            except Exception as e:
                print("❌ Myntra cart error:", e)

        else:
            print("❌ Unknown platform:", url)

    driver.quit()
    return f"🛒 Added {len(product_list)} item(s) to cart."