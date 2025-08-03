from crewai.tools import BaseTool
from backend.bots.cart_history_bot import search_user_cart_history

def get_cart_history_search_tool():
    class CartHistorySearchTool(BaseTool):
        name: str = "CartHistorySearchTool"
        description: str = (
            "Searches user's cart history based on specific queries. Can filter by product type, time range, or keywords."
        )

        def _run(self, user_id: int, search_query: str):
            print(f"🔧 Cart History Search Tool - User: {user_id}, Query: '{search_query}'")
            
            # Call the final function to search cart history
            result = search_user_cart_history(user_id, search_query)
            print(f"🟢 Cart History Search Result: Found {len(result.get('items', []))} matching items")
            return result

    return CartHistorySearchTool()