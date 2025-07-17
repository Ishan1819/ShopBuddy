from crewai.tools import BaseTool
from backend.bots.price_notifier_bot import schedule_daily_price_check

def get_price_drop_tool():
    class PriceDropTool(BaseTool):
        name: str = "PriceDropChecker"
        description: str = (
            "Checks the price of a product from an Amazon URL and sends daily emails if the price drops."
        )

        def _run(self, url: str, target_price: int = 3000):
            schedule_daily_price_check(url, target_price)
            return f"🔔 Price monitoring started for {url}. You'll be alerted if the price drops below ₹{target_price}."

    return PriceDropTool()
