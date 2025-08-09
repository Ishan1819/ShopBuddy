# # run_price_check.py
# import json
# from pathlib import Path
# from backend.bots.price_notifier_bot import schedule_daily_price_check

# PRODUCTS_FILE = Path("backend/utils/monitored_products.json")

# if PRODUCTS_FILE.exists():
#     with open(PRODUCTS_FILE, "r") as f:
#         products = json.load(f)
# else:
#     products = []

# if not products:
#     print("No products to monitor.")
# else:
#     for product in products:
#         schedule_daily_price_check(
#             url=product["url"],
#             target_price=product["target_price"],
#             user_id=product.get("user_id", "N/A")
#         )
