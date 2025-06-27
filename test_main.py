import json
from backend.crew_config.crew_setup import (
    create_parser_search_crew,
    create_addtocart_crew,
    create_price_drop_crew,
    create_buy_now_crew
)

def search_products_flow():
    user_query = input("🔍 What do you want to search? ").strip()
    if not user_query:
        print("⚠️ No query entered.")
        return

    # Step 1: Run parser + search crew
    parser_search_crew = create_parser_search_crew(user_query)
    parser_search_crew.kickoff()

    # Step 2: Access task output safely
    task_output = parser_search_crew.tasks[1].output
    try:
        if isinstance(task_output, str):
            search_results = json.loads(task_output)
        elif isinstance(task_output, dict):
            search_results = task_output
        elif hasattr(task_output, "model_dump"):
            search_results = task_output.model_dump().get("output", [])
        else:
            raise ValueError("❌ Unsupported output format.")
    except Exception as e:
        print(f"❌ Failed to parse product list: {e}")
        return

    if not isinstance(search_results, list):
        print("❌ Unexpected format of search results.")
        return

    # Display top products
    print("\n🛍️ Top 15 Products:\n")
    for idx, product in enumerate(search_results, 1):
        print(f"{idx}. {product['title'][:60]}...\n   💰 {product.get('price', 'N/A')} | 🔗 {product['url']}\n")

def add_to_cart_flow():
    url = input("🛒 Enter the product URL to add to cart: ").strip()
    if url:
        cart_crew = create_addtocart_crew(url)
        cart_crew.kickoff()

def price_notifier_flow():
    url = input("🔔 Enter the product URL for price drop notifications: ").strip()
    if url:
        price_drop_crew = create_price_drop_crew(url)
        price_drop_crew.kickoff()

def buy_now_flow():
    print("💳 Proceeding to buy now...")
    buy_crew = create_buy_now_crew()
    buy_crew.kickoff()


def main():
    print("🛒 Welcome to ShopBuddyAI!")

    while True:
        print("\n🔧 What would you like to do?")
        print("1. Search for products")
        print("2. Add a product to cart directly")
        print("3. Set a price drop notifier")
        print("4. Buy items from the cart")
        print("5. Exit")

        choice = input("Choose an option [1-5]: ").strip()

        if choice == '1':
            search_products_flow()
        elif choice == '2':
            add_to_cart_flow()
        elif choice == '3':
            price_notifier_flow()
        elif choice == '4':
            buy_now_flow()
        elif choice == '5':
            print("👋 Exiting ShopBuddyAI. See you again!")
            break
        else:
            print("❌ Invalid choice. Please enter a number from 1 to 5.")

if __name__ == "__main__":
    main()
