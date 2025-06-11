# ...existing code...
from backend.nlp.parser import parse_user_query_with_gemini
from backend.bots.amazon_bot import search_amazon
from backend.bots.flipkart_bot import search_flipkart
from backend.bots.myntra_bot import search_myntra
from backend.bots.amazon_bot import add_to_cart_amazon
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from backend.bots.flipkart_bot import add_to_cart_flipkart
from backend.bots.myntra_bot import add_to_cart_myntra

if __name__ == "__main__":
    user_query = input("Enter your shopping query: ")

    filters = parse_user_query_with_gemini(user_query)

    print("Parsed filters:", filters)

    platforms = filters["platform"]
    if isinstance(platforms, str):
        platforms = [platforms]

    all_results = {}

    for platform in platforms:
        platform = platform.lower()
        if platform == "amazon":
            results = search_amazon(filters)
            all_results["amazon"] = results
        elif platform == "flipkart":
            results = search_flipkart(filters)
            all_results["flipkart"] = results
        elif platform == "myntra":
            results = search_myntra(filters)
            all_results["myntra"] = results

    if all_results:
        for plat, results in all_results.items():
            print(f"\nTop Results from {plat.capitalize()}:")
            for idx, item in enumerate(results, start=1):
                print(f"{idx}. {item['title']}\n   {item['url']}\n")
    else:
        print("No supported platforms found.")

    # ...existing code...
    print("Search completed. Do you want to add items to cart? (yes/no)")
    if input().strip().lower() == "yes":
        print("Please put the url of the product you want to add to cart:")
        url_input = input().strip()
        options = Options()
        options.add_argument("--headless=false")
        driver = webdriver.Chrome(options=options)
        if "amazon" in url_input:
            add_to_cart_amazon(driver, url_input)
        elif "flipkart" in url_input:
            add_to_cart_flipkart(driver, url_input)
        elif "myntra" in url_input:
            add_to_cart_myntra(driver, url_input)
        else:
            print("Currently, only Amazon, Flipkart, and Myntra add-to-cart are supported for direct URLs.")
        driver.quit()
# ...existing code...