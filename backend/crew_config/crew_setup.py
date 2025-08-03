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
from backend.tools.cart_search_tool import get_cart_search_tool
from backend.tools.signin_signup_tool import get_signin_signup_tool
from backend.tools.cart_history_tool import get_cart_history_search_tool
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


def create_addtocart_crew(product_url: str, user_id: int) -> Crew:
    cart_ai = Agent(
        role="Cart Agent",
        goal="Add selected product to the Amazon cart and save to database",
        backstory="Expert at handling automation for adding specific products to the cart and managing user data.",
        tools=[get_cart_tool()],
        verbose=True,
        llm=gemini_llm
    )

    cart_task = Task(
        description=f"Add this product to the cart: '{product_url}' for user ID: {user_id}. Make sure to save the product details to the database.",
        agent=cart_ai,
        expected_output="Confirmation of product added to cart and saved to database with user information.",
        # Pass both URL and user_id to the task
        input={"product_url": product_url, "user_id": user_id}
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



def create_search_cart_crew(user_query: str, login_id: int) -> Crew:
    search_cart = Agent(
        role="Search Cart Agent",
        goal="Search for products and display to the user",
        backstory="An expert in searching products and displaying them to the user.",
        tools=[get_cart_search_tool()],
        verbose=True,
        llm=gemini_llm
    )
    
    search_task = Task(
        description=f"Search for products based on user query from the cart: '{user_query}' for user with ID {login_id}.",
        agent=search_cart,
        expected_output="A list of product dictionaries with title, url, and price.",
        input={"query": user_query}
    )
    
    return Crew(
        agents=[search_cart],
        tasks=[search_task],
        process="sequential",
        verbose=True
    )
    

# Before wala code
# def signin_signup(email: str, password: str) -> Crew:
#     signin_ai = Agent(
#         role="SignIn/SignUp Agent",
#         goal="Handle user sign-in or sign-up",
#         backstory="An expert in managing user authentication.",
#         tools=[get_signin_signup_tool()],
#         verbose=True,
#         llm=gemini_llm
#     )
    
#     signin_task = Task(
#         description=f"Handle user authentication for email: {email} and password: {password}",  # ✅ Include params here
#         agent=signin_ai,
#         expected_output="A dictionary with status, message, and user_id if signed in or signed up.",
#         input={"email": email, "password": password} # 🔄 Pass params as
#         # "input"  # This allows the agent to use them directly
#     )
    
#     return Crew(
#         agents=[signin_ai],
#         tasks=[signin_task],
#         process="sequential",
#         verbose=True
#     )


def signin_signup(email: str, password: str) -> Crew:
    signin_ai = Agent(
        role="SignIn/SignUp Agent",
        goal="Handle user sign-in or sign-up",
        backstory="An expert in managing user authentication.",
        tools=[get_signin_signup_tool()],
        verbose=True,
        llm=gemini_llm
    )
    
    signin_task = Task(
        description=f"Use the SigninSignupTool to authenticate user with email '{email}' and password '{password}'. Return the exact result from the tool.",
        agent=signin_ai,
        expected_output="Return the exact dictionary result from the SigninSignupTool containing status, message, and user_id.",
        # Remove the input parameter as it might be causing issues
    )
    
    return Crew(
        agents=[signin_ai],
        tasks=[signin_task],
        process="sequential",
        verbose=True
    )



def create_cart_history_crew(user_id: int, search_query: str) -> Crew:
    """Create crew to handle cart history search and retrieval"""
    
    cart_history_ai = Agent(
        role="Cart History Search Agent",
        goal="Search and retrieve specific products from user's cart history based on their query",
        backstory="Expert at understanding user queries about their cart history and finding relevant products. Can interpret time-based queries (like 'hours before', 'yesterday') and product-based queries (like 'shoes', 'handbags', 'electronics').",
        tools=[get_cart_history_search_tool()],
        verbose=True,
        llm=gemini_llm
    )

    cart_history_task = Task(
        description=f"""
        Search the cart history for user ID: {user_id} based on this query: "{search_query}"
        
        Instructions:
        1. Analyze the user's query to understand what they're looking for
        2. If the query mentions time (like "hours before", "yesterday", "last week"), filter by time range
        3. If the query mentions specific products (like "shoes", "bags", "electronics"), filter by product description
        4. Return only the matching products with their timestamps, descriptions, prices, and URLs
        5. If no matches found, explain what was searched and suggest alternatives
        
        Format the response in a user-friendly way showing only relevant results.
        """,
        agent=cart_history_ai,
        expected_output="A filtered list of cart items matching the user's query, with timestamp, product description, price, and URL for each relevant item.",
        input={"user_id": user_id, "search_query": search_query}
    )

    return Crew(
        agents=[cart_history_ai],
        tasks=[cart_history_task],
        process="sequential",
        verbose=True
    )