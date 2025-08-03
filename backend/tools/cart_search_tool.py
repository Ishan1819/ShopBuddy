from crewai.tools import BaseTool
from backend.bots.search_cart_bot import search_products  # Adjust if your path differs
def get_cart_search_tool():
    class CartSearchTool(BaseTool):
        name: str = "CartSearch"
        description: str = "Adds selected products to the shopping cart"

        def _run(self, query: str, login_id: int):
            print("🛒 Searching products from the cart...")
            return search_products(query,  login_id)  # Top 3 only

    return CartSearchTool()