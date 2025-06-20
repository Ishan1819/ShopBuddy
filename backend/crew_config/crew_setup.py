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
