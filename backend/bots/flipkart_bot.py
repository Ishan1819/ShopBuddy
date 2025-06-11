# backend/bots/flipkart_bot.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from urllib.parse import quote_plus

def search_flipkart(filters):
    options = Options()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)

    query = f"{filters['brand']} {filters['color']} {filters['category']}"
    url = f"https://www.flipkart.com/search?q={quote_plus(query)}"
    driver.get(url)
    time.sleep(3)

    # Close login popup if it appears
    try:
        close_btn = driver.find_element(By.XPATH, "//button[contains(text(),'✕')]")
        close_btn.click()
    except:
        pass

    results = []
    products = driver.find_elements(By.XPATH, "//a[contains(@href, '/p/')]")
    seen = set()
    for product in products[:10]:
        try:
            title = product.text.strip()
            link = "https://www.flipkart.com" + product.get_attribute("href")
            if link not in seen and title:
                results.append({"title": title, "url": link})
                seen.add(link)
        except Exception:
            continue

    driver.quit()
    return results

# ✅ Test it
# if __name__ == "__main__":
#     test_filters = {
#         "platform": "flipkart",
#         "category": "jeans",
#         "brand": "Levis",
#         "color": "blue",
#         "material": "any",
#         "min_price": 1000,
#         "max_price": 3000,
#         "min_rating": 4.0
#     }
#     print(search_flipkart(test_filters))
