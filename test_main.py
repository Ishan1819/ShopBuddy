# from backend.crew_config.crew_setup import create_crew

# if __name__ == "__main__":
#     print("🛒 Welcome to ShopBuddyAI!")
#     user_query = input("Enter your shopping request: ")
#     print(user_query)
#     crew = create_crew(user_query)

#     print("\n🤖 Crew is working on your query...")
#     result = crew.kickoff()
#     print("\n✅ Result:\n", result)






import json
from backend.crew_config.crew_setup import create_parser_search_crew, create_addtocart_crew, create_price_drop_crew

def main():
    print("🛒 Welcome to ShopBuddyAI!")
    user_query = input("Enter your shopping request: ").strip()

    if not user_query:
        print("⚠️ No query entered.")
        return

    # Step 1: Run parser + search crew
    parser_search_crew = create_parser_search_crew(user_query)
    parser_search_crew.kickoff()

    # Step 2: Access task output safely
    task_output = parser_search_crew.tasks[1].output
    print("🧪 Task 2 Output:", task_output)
    print(type(task_output))

    
    # Try parsing from string
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

    # Step 3: Display top products
    print("\n🛍️ Top 15 Products:\n")
    for idx, product in enumerate(search_results, 1):
        print(f"{idx}. {product['title'][:60]}...\n   💰 {product.get('price', 'N/A')} | 🔗 {product['url']}\n")

    check = input("Press 1 for adding to cart, Press 2 for price drop notifier, or any other key to exit: ").strip()
    if check == '1':
        print("🛒 Proceeding to add product to cart...")
        selected_url = input("\n🛒 Enter the URL of the product you want to add to the cart: ").strip()
        if selected_url:
            cart_crew = create_addtocart_crew(selected_url)
            cart_crew.kickoff()
    elif check == '2':
        url = input("Enter the product URL for price drop notifications: ").strip()
        if url:
            print("🔔 Setting up price drop notifier for:", url)
            price_drop_crew = create_price_drop_crew(url)
            price_drop_crew.kickoff()
    else:
        print("❌ Exiting without adding to cart or setting up price drop notifier.")
        return

    # Step 4: Ask user for product URL to add to cart
    

if __name__ == "__main__":
    main()
