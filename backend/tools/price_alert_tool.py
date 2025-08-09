from crewai.tools import BaseTool
from pydantic import Field
from backend.bots.price_notifier_bot import schedule_daily_price_check


def get_price_alert_tool():
    class PriceDropTool(BaseTool):
        name: str = "PriceDropChecker"
        description: str = (
            "Monitors the price of a product using its Amazon URL and sends an email "
            "alert when the price drops below the specified threshold."
        )

        def _run(self, url: str, target_price: int, user_id: int):
            try:
                schedule_daily_price_check(url, target_price, user_id)
                return (
                    f"✅ Price monitoring started for:\n📦 {url}\n"
                    f"You'll be notified if the price drops below ₹{target_price}."
                )
            except Exception as e:
                return f"❌ Failed to schedule price check: {str(e)}"

    return PriceDropTool()
