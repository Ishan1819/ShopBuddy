# tools/buy_now_tool.py
# from crewai.tools import BaseTool
# from backend.bots.buy_now_bot import proceed_to_checkout

# def get_buy_now_tool():
#     class BuyNowTool(BaseTool):
#         name: str = "BuyNowExecutor"
#         description: str = "Automates checkout, address input, and payment selection."

#         def _run(self):
#             # Now ignores input_data and collects from user inside bot
#             name = input("Enter your full name: ")
#             phone = input("Enter your phone number: ")
#             address = input("Enter your address: ")
#             payment_choice = int(input("Enter your payment choice (1: 'Credit or Debit Card', 2: 'Net banking', 3: 'EMI', 4: 'Other UPI apps', 5: 'Cash on Delivery'): "))
#             print("🛍️ This is the payment choice:", payment_choice)
#             return proceed_to_checkout(name, phone, address, payment_choice)

#     return BuyNowTool()














from crewai.tools import BaseTool
from backend.bots.buy_now_bot import proceed_to_checkout  # Adjust if your path differs

def get_buy_now_tool():
    class BuyNowTool(BaseTool):
        name: str = "BuyNowExecutor"
        description: str = (
            "Automates the Amazon checkout process. "
            "Handles address autofill (if missing), Gemini parsing, and payment choice."
        )

        def _run(self):
            try:
                payment_choice = int(input("payment_choice"))

                if not all([payment_choice]):
                    return "❌ Missing one or more required fields: name, phone, address, payment_choice."

                result = proceed_to_checkout(payment_choice)
                return result

            except Exception as e:
                return f"❌ Error during BuyNowTool execution: {str(e)}"

    return BuyNowTool()
