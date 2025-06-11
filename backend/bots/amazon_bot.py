# backend/bots/amazon_bot.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from urllib.parse import quote_plus

def search_amazon(filters):
    options = Options()
    options.add_argument("--headless=new")  # run headless
    driver = webdriver.Chrome(options=options)

    query = f"{filters['brand']} {filters['color']} {filters['category']}"
    url = f"https://www.amazon.in/s?k={quote_plus(query)}"
    driver.get(url)
    time.sleep(3)

    # Apply filters manually if needed (e.g., price)
    try:
        # Set price range if specified
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
    for product in products[:20]:
        try:
            title = product.find_element(By.TAG_NAME, "h2").text
            link = product.find_element(By.TAG_NAME, "a").get_attribute("href")
            results.append({"title": title, "url": link})
        except Exception:
            continue

    driver.quit()
    return results

# # ✅ Test it
# if __name__ == "__main__":
#     test_filters = {
#         "platform": "amazon",
#         "category": "shoes",
#         "brand": "Nike",
#         "color": "black",
#         "material": "any",
#         "min_price": 0,
#         "max_price": 2000,
#         "min_rating": 4.0
#     }
#     print(search_amazon(test_filters))




