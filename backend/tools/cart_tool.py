from crewai.tools import BaseTool
from backend.bots.cart_bot import add_to_cart

def get_cart_tool():
    class CartAdderTool(BaseTool):
        name: str = "CartAdder"
        description: str = "Adds selected products to the shopping cart"

        def _run(self, product_list: list):
            print("🛒 Adding products to cart...")
            return add_to_cart(product_list[:3])  # Top 3 only

    return CartAdderTool()
