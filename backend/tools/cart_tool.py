from crewai.tools import BaseTool
from backend.bots.cart_bot import add_to_cart

def get_cart_tool():
    class CartTool(BaseTool):
        name: str = "CartTool"
        description: str = (
            "Adds products to cart and saves to database. Requires product URL and user ID."
        )

        def _run(self, product_url: str, user_id: int):
            print(f"🔧 Cart Tool - Adding product: {product_url}")
            print(f"🔧 Cart Tool - User ID: {user_id}")
            
            # Call the updated add_to_cart function with user_id
            result = add_to_cart(product_url, user_id=user_id)
            print(f"🟢 Cart Tool Result: {result}")
            return result

    return CartTool()
