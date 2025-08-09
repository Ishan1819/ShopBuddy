# backend/utils/price_alert_utils.py

import requests
from bs4 import BeautifulSoup
import smtplib
from email.message import EmailMessage

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-US,en;q=0.9",
}

def get_price_from_amazon(url: str) -> int:
    response = requests.get(url, headers=headers, timeout=15)
    soup = BeautifulSoup(response.text, "html.parser")

    price_tag = soup.select_one("span.a-price-whole")
    if not price_tag:
        raise ValueError("Price not found on page")
    
    price_text = price_tag.get_text().replace(",", "").strip()
    return int(price_text)

def send_price_alert_email(product_url: str, current_price: int, target_price: int, price_dropped: bool):
    msg = EmailMessage()
    msg["From"] = "ishanp141@gmail.com"
    msg["To"] = "ishan.patil23@pccoepune.org"

    if price_dropped:
        msg["Subject"] = "🔔 Price Drop Alert!"
        msg.set_content(
            f"The price for the product at:\n{product_url}\n"
            f"has dropped to ₹{current_price}, which is below your target of ₹{target_price}!"
        )
    else:
        msg["Subject"] = "📊 Price Check Update (No Drop)"
        msg.set_content(
            f"The current price for the product at:\n{product_url}\n"
            f"is ₹{current_price}, which is still above your target of ₹{target_price}.\n"
            f"We'll keep checking every 5 minutes!"
        )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login("ishanp141@gmail.com", "jpxb xscs hhqs evqj")
        smtp.send_message(msg)

