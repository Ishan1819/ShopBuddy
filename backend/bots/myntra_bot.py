# backend/bots/myntra_bot.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from urllib.parse import quote_plus

def search_myntra(filters):
    options = Options()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)

    query = f"{filters['brand']} {filters['color']} {filters['category']}"
    url = f"https://www.myntra.com/{quote_plus(query)}"
    driver.get(url)
    time.sleep(3)

    results = []
    products = driver.find_elements(By.XPATH, "//li[@class='product-base']")
    for product in products[:10]:
        try:
            title_el = product.find_element(By.CLASS_NAME, "product-product")
            brand_el = product.find_element(By.CLASS_NAME, "product-brand")
            link_el = product.find_element(By.TAG_NAME, "a")
            title = f"{brand_el.text.strip()} {title_el.text.strip()}"
            link = link_el.get_attribute("href")
            results.append({"title": title, "url": link})
        except Exception:
            continue

    driver.quit()
    return results

# ✅ Test it
# if __name__ == "__main__":
#     test_filters = {
#         "platform": "myntra",
#         "category": "t-shirt",
#         "brand": "H&M",
#         "color": "white",
#         "material": "any",
#         "min_price": 500,
#         "max_price": 2000,
#         "min_rating": 4.0
#     }
#     print(search_myntra(test_filters))
