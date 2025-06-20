import time
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ---- CONFIG ----
DEFAULT_TARGET_PRICE = 4000  # fallback
RECIPIENT_EMAIL = "feyoni19@gmail.com"
SENDER_EMAIL = "ishanp141@gmail.com"
SENDER_PASSWORD = "tmlfdgrldnmvdmfw"  # Gmail App Password


# ---- SCRAPER ----
def get_price_from_amazon(url: str):
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)
        time.sleep(3)

        price_selectors = [
            "//span[@class='a-price-whole']",
            "//span[contains(@class, 'a-price-whole')]",
            "//span[@class='a-offscreen']"
        ]

        for selector in price_selectors:
            try:
                price_elem = driver.find_element(By.XPATH, selector)
                price_text = price_elem.text.replace(",", "").replace("₹", "").strip()
                if price_text and price_text.replace('.', '', 1).isdigit():
                    return int(float(price_text))
            except:
                continue

        return None
    finally:
        driver.quit()


# ---- EMAIL NOTIFICATIONS ----
def send_email(to_email: str, subject: str, body: str):
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, to_email, msg.as_string())
        server.quit()
        print(f"✅ Email sent to {to_email}")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")


# ---- CONFIRMATION EMAIL ----
def send_confirmation_email(url, target_price):
    subject = "🔔 Price Drop Alert Activated!"
    body = f"""
    You've asked us to watch this product on Amazon:

    🔗 Product URL: {url}
    🎯 Target Price: ₹{target_price}

    We'll notify you once it drops below the target price. Happy shopping!
    """
    print("📧 Sending confirmation email...")
    send_email(RECIPIENT_EMAIL, subject, body)


# ---- PRICE CHECK AND ALERT ----
def check_price_and_notify(url: str, target_price: int = DEFAULT_TARGET_PRICE):
    print(f"🔍 Checking price for: {url}")
    current_price = get_price_from_amazon(url)

    if current_price is None:
        return {"status": "failed", "reason": "Price not found"}

    print(f"💰 Current price: ₹{current_price} | Target: ₹{target_price}")
    if current_price <= target_price:
        subject = "📉 Amazon Price Drop Alert!"
        body = f"""
        Good news! The price for your watched product has dropped!

        🔗 Product URL: {url}
        💰 Current Price: ₹{current_price}
        🎯 Target Price: ₹{target_price}

        Hurry before it's gone!
        """
        send_email(RECIPIENT_EMAIL, subject, body)
        return {"status": "alert_sent", "current_price": current_price}
    else:
        return {"status": "no_drop", "current_price": current_price}


# ---- DAILY MONITORING ----
def schedule_daily_price_check(url: str, target_price: int, delay_seconds: int = 86400):
    """
    Schedule price check every 24 hours (or shorter delay for testing).
    Sends confirmation email immediately.
    """
    # def monitor():
    #     result = check_price_and_notify(url, target_price)
    #     print("🕒 Daily price check result:", result)
    #     # Re-schedule
    #     threading.Timer(delay_seconds, monitor).start()

    send_confirmation_email(url, target_price)
    # print("✅ Monitoring scheduled. First check will run in", delay_seconds, "seconds.")
    # threading.Timer(10, monitor).start()  # 10 seconds delay for first run

    return {
        "status": "monitoring_started",
        "target_price": target_price,
        "url": url,
        "next_check_in_seconds": delay_seconds
    }
