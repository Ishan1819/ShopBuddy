# # tools/buy_now_tool.py
# from crewai.tools import BaseTool
# from backend.bots.buy_now_bot import proceed_to_checkout

# def get_buy_now_tool():
#     class BuyNowTool(BaseTool):
#         name: str = "BuyNowExecutor"
#         description: str = "Automates checkout, address input, and payment selection."

#         def _run(self, input_data: dict):
#             name = input_data.get("name")
#             phone = input_data.get("phone")
#             address = input_data.get("address")
#             payment_choice = input_data.get("payment_choice")
#             print("🛍️ Thisis the payemnt choice", payment_choice)
#             return proceed_to_checkout(name, phone, address, payment_choice)

#     return BuyNowTool()




# tools/buy_now_tool.py
from crewai.tools import BaseTool
from backend.bots.buy_now_bot import proceed_to_checkout

def get_buy_now_tool():
    class BuyNowTool(BaseTool):
        name: str = "BuyNowExecutor"
        description: str = "Automates checkout, address input, and payment selection."

        def _run(self):
            # Now ignores input_data and collects from user inside bot
            name = input("Enter your full name: ")
            phone = input("Enter your phone number: ")
            address = input("Enter your address: ")
            payment_choice = int(input("Enter your payment choice (1: 'Credit or Debit Card', 2: 'Net banking', 3: 'EMI', 4: 'Other UPI apps', 5: 'Cash on Delivery'): "))
            print("🛍️ This is the payment choice:", payment_choice)
            return proceed_to_checkout(name, phone, address, payment_choice)

    return BuyNowTool()
