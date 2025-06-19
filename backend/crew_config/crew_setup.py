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
#         goal="Find the best mat ching products based on parsed filters",
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

#     task1 = Task(
#         description=(
#             "Parse the user query into structured product filters "
#             "using the QueryParser tool. The tool will extract fields like platform, color, brand, etc."
#         ),
#         agent=parser_ai,
#         input=user_query,
#         expected_output=(
#             "A dictionary with keys like platform, brand, category, color, min_price, max_price, gender"
#         )
#     )


#     task2 = Task(
#         description="Use those filters to search product URLs.",
#         agent=search_ai,
#         input=lambda memory: {"filters": memory["task1"]},  # <-- Pass output of task1 as filters
#         expected_output="A list of product URLs with titles and prices."
#     )

#     task3 = Task(
#         description="Add top 3 results to cart.",
#         agent=cart_ai,
#         input=lambda memory: {"products": memory["task2"]},  # <-- Pass output of task2
#         expected_output="A confirmation that the top 3 products were added to the cart."
#     )
# # ...existing code...

#     # === Crew ===
#     return Crew(
#         agents=[parser_ai, search_ai, cart_ai],
#         tasks=[task1, task2, task3],
#         process="sequential"
#     )





# backend/crew_config/crew_setup.py
from crewai import Agent, Task, Crew
from backend.llm.litellm_wrapper import LiteLLMWrapper
from backend.tools.parser_tool import get_parser_tool
from backend.tools.search_tool import get_search_tool
# from backend.tools.cart_tool import get_cart_tool

# Use litellm-wrapped Gemini
gemini_llm = LiteLLMWrapper(model="gemini/gemini-1.5-flash")

def create_crew(user_query: str) -> Crew:
    # print("🛒 Creating Crew for user query:", user_query)
    
    # === Agents ===
    parser_ai = Agent(
        role="Query Parser",
        goal="Convert user queries into structured filters",
        backstory="Trained in understanding e-commerce user intent and structuring it.",
        tools=[get_parser_tool()],
        verbose=True,
        llm=gemini_llm
    )
    
    search_ai = Agent(
        role="Product Searcher", 
        goal="Find the best matching products based on parsed filters and also search them on Amazon, Flipkart, and Myntra.",
        backstory="Expert in using parsed filters to search Amazon, Flipkart, and Myntra.",
        tools=[get_search_tool()],
        verbose=True,
        llm=gemini_llm
    )
    
    # cart_ai = Agent(
    #     role="Cart Handler",
    #     goal="Add the best items to cart from the product results",
    #     backstory="Handles automation for adding products to carts.",
    #     tools=[get_cart_tool()],    
    #     verbose=True,
    #     llm=gemini_llm
    # )
    
    # === Tasks ===
    task1 = Task(
        description=f"Parse this user query into structured product filters: '{user_query}'. Extract platform, brand, category, color, min_price, max_price, gender, and other relevant filters.",
        agent=parser_ai,
        expected_output="A dictionary with keys like platform, brand, category, color, min_price, max_price, gender"
    )
    
    task2 = Task(
        description="Use those filters to search product URLs.",
        agent=search_ai,
        expected_output="A list of product URLs with titles and prices.",
        context=[task1]  # This tells CrewAI that this task depends on task1's output
    )
    
    # task3 = Task(
    #     description="Add the top 3 products from the search results to the cart. Use the product list from the previous task.",
    #     agent=cart_ai,
    #     expected_output="A confirmation that the top 3 products were added to the cart.",
    #     context=[task2]  # This tells CrewAI that this task depends on task2's output
    # )
    
    # === Crew ===
    # return Crew(
    #     agents=[parser_ai, search_ai, cart_ai],
    #     tasks=[task1, task2, task3],
    #     process="sequential",
    #     verbose=True
    # )

    return Crew(
        agents=[parser_ai, search_ai],
        tasks=[task1, task2],
        process="sequential",
        verbose=True
    )