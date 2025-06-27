# # backend/crew_config/crew_setup.py
# from crewai import Agent, Task, Crew
# from backend.llm.litellm_wrapper import LiteLLMWrapper
# from backend.tools.parser_tool import get_parser_tool
# from backend.tools.search_tool import get_search_tool
# from backend.tools.cart_tool import get_cart_tool

# # Use litellm-wrapped Gemini
# gemini_llm = LiteLLMWrapper(model="gemini/gemini-1.5-flash")

# def create_crew(user_query: str) -> Crew:
#     # print("🛒 Creating Crew for user query:", user_query)
    
#     # === Agents ===
#     parser_ai = Agent(
#         role="Query Parser",
#         goal="Convert user queries into structured filters",
#         backstory="Trained in understanding e-commerce user intent and structuring it.",
#         tools=[get_parser_tool()],
#         verbose=True,
#         llm=gemini_llm
#     )
    
#     search_ai = Agent(
#         role="Product Searcher", 
#         goal="Find the best matching products based on parsed filters and also search them on Amazon, Flipkart, and Myntra.",
#         backstory="Expert in using parsed filters to search Amazon, Flipkart, and Myntra.",
#         tools=[get_search_tool()],
#         verbose=True,
#         llm=gemini_llm
#     )
    
#     cart_ai = Agent(
#         role="Cart Handler",
#         goal="Add the best items to cart from the product results",
#         backstory="Handles automation for adding products to carts.",
#         tools=[get_cart_tool()],    
#         verbose=True,
#         llm=gemini_llm
#     )
    
#     # === Tasks ===
#     task1 = Task(
#         description=f"Parse this user query into structured product filters: '{user_query}'. Extract platform, brand, category, color, min_price, max_price, gender, and other relevant filters.",
#         agent=parser_ai,
#         expected_output="A dictionary with keys like platform, brand, category, color, min_price, max_price, gender"
#     )
    
#     task2 = Task(
#         description="Use those filters to search product URLs.",
#         agent=search_ai,
#         expected_output="A list of product URLs with titles and prices.",
#         context=[task1]  # This tells CrewAI that this task depends on task1's output
#     )
    
#     task3 = Task(
#         description="Add the top 3 products from the search results to the cart. Use the product list from the previous task.",
#         agent=cart_ai,
#         expected_output="A confirmation that the top 3 products were added to the cart.",
#         context=[task2]  # This tells CrewAI that this task depends on task2's output
#     )
    
#     # === Crew ===
#     return Crew(
#         agents=[parser_ai, search_ai, cart_ai],
#         tasks=[task1, task2, task3],
#         process="sequential",
#         verbose=True
#     )

#     # return Crew(
#     #     agents=[parser_ai, search_ai],
#     #     tasks=[task1, task2],
#     #     process="sequential",
#     #     verbose=True
#     # )








from crewai import Agent, Task, Crew
from backend.llm.litellm_wrapper import LiteLLMWrapper
from backend.tools.parser_tool import get_parser_tool
from backend.tools.search_tool import get_search_tool
from backend.tools.cart_tool import get_cart_tool
from backend.tools.price_drop_tool import get_price_drop_tool
from backend.tools.buy_now_tool import get_buy_now_tool

gemini_llm = LiteLLMWrapper(model="gemini/gemini-1.5-flash")

def create_parser_search_crew(user_query: str) -> Crew:
    parser_ai = Agent(
        role="Query Parser",
        goal="Convert user queries into structured filters",
        backstory="Expert at structuring e-commerce filters.",
        tools=[get_parser_tool()],
        verbose=True,
        llm=gemini_llm
    )

    search_ai = Agent(
        role="Product Searcher",
        goal="Find matching products based on filters.",
        backstory="Expert in searching Amazon products.",
        tools=[get_search_tool()],
        verbose=True,
        llm=gemini_llm
    )

    task1 = Task(
        description=f"Parse this user query into structured filters: '{user_query}'. Extract platform, brand, category, color, min_price, max_price, gender, etc.",
        agent=parser_ai,
        expected_output="A dictionary with platform, brand, category, color, min_price, max_price, gender, etc."
    )

    task2 = Task(
        description="Use those filters to search product URLs on Amazon.",
        agent=search_ai,
        expected_output="A list of 15 product dictionaries with title, url, and price.",
        context=[task1]
    )

    return Crew(
        agents=[parser_ai, search_ai],
        tasks=[task1, task2],
        process="sequential",
        verbose=True
    )


def create_addtocart_crew(product_url: str) -> Crew:
    cart_ai = Agent(
        role="Cart Agent",
        goal="Add selected product to the Amazon cart",
        backstory="Expert at handling automation for adding specific products to the cart.",
        tools=[get_cart_tool()],
        verbose=True,
        llm=gemini_llm
    )

    cart_task = Task(
        description=f"Add this product to the cart: '{product_url}'",
        agent=cart_ai,
        expected_output="Confirmation of product added to cart."
    )

    return Crew(
        agents=[cart_ai],
        tasks=[cart_task],
        process="sequential",
        verbose=True
    )

def create_price_drop_crew(product_url: str) -> Crew:
    # Placeholder for price drop notifier crew
    # This would be similar to the addtocart crew but focused on monitoring price drops
    price_drop_ai = Agent(
        role="Price Drop Notifier",
        goal="Notify user when the price drops for a specific product",
        backstory="Expert at monitoring product prices and notifying users.",
        tools=[get_price_drop_tool()],  # Assuming get_cart_tool() can handle price monitoring
        verbose=True,
        llm=gemini_llm
    )
    price_drop_task = Task(
        description=f"Monitor price drop for product: '{product_url}'",
        agent=price_drop_ai,
        expected_output="Notification when the price drops."
    )

    return Crew(
        agents=[price_drop_ai],
        tasks=[price_drop_task],
        process="sequential",
        verbose=True
    )


# def create_buy_now_crew(name, phone, address, payment_choice) -> Crew:
#     buy_ai = Agent(
#         role="Cart Buyer",
#         goal="Complete the purchase of items in the Amazon cart",
#         backstory="An expert in automating the checkout process on Amazon, capable of handling address entry and payment methods.",
#         tools=[get_buy_now_tool()],
#         verbose=True,
#         llm=gemini_llm
#     )

#     buy_task = Task(
#         description="Complete the checkout with provided address and selected payment method.",
#         agent=buy_ai,
#         expected_output="Order placed or redirected to payment page.",
#         input={
#             "name": name,
#             "phone": phone,
#             "address": address,
#             "payment_choice": payment_choice
#         }
#     )   

#     return Crew(
#         agents=[buy_ai],
#         tasks=[buy_task],
#         process="sequential",
#         verbose=True
#     )




def create_buy_now_crew() -> Crew:
    buy_ai = Agent(
        role="Cart Buyer",
        goal="Complete the purchase of items in the Amazon cart",
        backstory="An expert in automating the checkout process on Amazon, capable of handling address entry and payment methods.",
        tools=[get_buy_now_tool()],
        verbose=True,
        llm=gemini_llm
    )

    buy_task = Task(
        description="Interactively collect address and payment info, then complete checkout.",
        agent=buy_ai,
        expected_output="Order placed or redirected to payment page.",
        input={}  # 🔄 No more pre-filled inputs
    )

    return Crew(
        agents=[buy_ai],
        tasks=[buy_task],
        process="sequential",
        verbose=True
    )
