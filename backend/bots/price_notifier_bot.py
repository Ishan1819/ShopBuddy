# import time
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# import signal
# import sys
# import os
# import json
# from datetime import datetime
# import subprocess
# import threading
# import time
# from datetime import datetime, timedelta
# # ---- CONFIG ----
# DEFAULT_TARGET_PRICE = 4000
# RECIPIENT_EMAIL = "ishan.patil23@pccoepune.org"
# SENDER_EMAIL = "ishanp141@gmail.com"
# SENDER_PASSWORD = "tmlfdgrldnmvdmfw"

# # Global flag for graceful shutdown
# running = True
# MONITOR_FILE = "price_monitor_config.json"

# # ---- GRACEFUL SHUTDOWN HANDLER ----
# def signal_handler(signum, frame):
#     global running
#     print(f"\n[STOP] Received signal {signum}. Stopping foreground session...")
#     running = False
    
#     # Check if background monitoring is active
#     config = load_monitor_config()
#     if config and config.get('status') == 'checking':
#         print("[INFO] Background monitoring will continue running...")
#         print("[INFO] Your price monitoring is still active in the background.")
#         print("[INFO] You'll continue receiving email notifications.")
#         print(f"[INFO] Monitoring: {config.get('url', 'N/A')}")
#         print(f"[INFO] Target Price: Rs.{config.get('target_price', 'N/A')}")
#     else:
#         print("[INFO] No background monitoring detected.")
    
#     print("[INFO] Foreground session ended. You can safely close the terminal.")
#     # sys.exit(0)

# # Register signal handlers
# signal.signal(signal.SIGINT, signal_handler)
# signal.signal(signal.SIGTERM, signal_handler)

# # ---- PERSISTENCE MANAGEMENT ----
# def save_monitor_config(url, target_price, interval_seconds):
#     """Save monitoring configuration to file"""
#     config = {
#         "url": url,
#         "target_price": target_price,
#         "interval_seconds": interval_seconds,
#         "start_time": datetime.now().isoformat(),
#         "status": "active"
#     }
    
#     with open(MONITOR_FILE, 'w') as f:
#         json.dump(config, f, indent=2)
    
#     print(f"[CONFIG] Monitor configuration saved to {MONITOR_FILE}")

# def load_monitor_config():
#     """Load monitoring configuration from file"""
#     if os.path.exists(MONITOR_FILE):
#         with open(MONITOR_FILE, 'r') as f:
#             return json.load(f)
#     return None

# def update_monitor_status(status):
#     """Update monitor status in config file"""
#     if os.path.exists(MONITOR_FILE):
#         with open(MONITOR_FILE, 'r') as f:
#             config = json.load(f)
        
#         config['status'] = status
#         config['last_update'] = datetime.now().isoformat()
        
#         with open(MONITOR_FILE, 'w') as f:
#             json.dump(config, f, indent=2)

# # ---- STATUS CHECKER ----
# def check_monitor_status():
#     """Check if monitoring is active"""
#     config = load_monitor_config()
#     if config:
#         print(f"[STATUS] Monitor Status: {config.get('status', 'unknown')}")
#         print(f"[STATUS] URL: {config.get('url', 'N/A')}")
#         print(f"[STATUS] Target Price: Rs.{config.get('target_price', 'N/A')}")
#         print(f"[STATUS] Check Interval: {config.get('interval_seconds', 'N/A')} seconds")
#         print(f"[STATUS] Started: {config.get('start_time', 'N/A')}")
#         print(f"[STATUS] Last Update: {config.get('last_update', 'N/A')}")
#         return config
#     else:
#         print("[ERROR] No active monitoring configuration found.")
#         return None

# # ---- BACKGROUND SERVICE METHODS ----
# def create_service_script(url, target_price, interval_seconds):
#     """Create a separate Python script for background monitoring"""
#     service_script = f"""
# import time
# import sys
# import os
# import signal
# import json
# from datetime import datetime

# # Ignore interrupt signals to prevent background process from stopping
# signal.signal(signal.SIGINT, signal.SIG_IGN)
# signal.signal(signal.SIGTERM, signal.SIG_IGN)

# sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# # Import all the monitoring functions
# from backend.bots.{os.path.basename(__file__).replace('.py', '')} import check_price_and_notify, send_email, update_monitor_status

# def background_monitor():
#     url = "{url}"
#     target_price = {target_price}
#     interval_seconds = {interval_seconds}
    
#     print(f"[BACKGROUND] Background monitoring started for: {{url}}")
#     print(f"[BACKGROUND] Target Price: Rs.{{target_price}}")
#     print(f"[BACKGROUND] Check Interval: {{interval_seconds}} seconds")
    
#     # Update status to show it's running in background
#     update_monitor_status("background_active")
    
#     while True:
#         try:
#             check_price_and_notify(url, target_price)
#             time.sleep(interval_seconds)
#         except Exception as e:
#             print(f"[ERROR] Error in background monitoring: {{e}}")
#             # Continue monitoring even if there's an error
#             time.sleep(interval_seconds)

# """
    
#     with open("background_monitor.py", "w") as f:
#         f.write(service_script)
    
#     print("[INFO] Background monitoring script created: background_monitor.py")
#     return "background_monitor.py"

# def start_background_process(script_path):
#     """Start background monitoring process"""
#     try:
#         # Start background process that's completely detached from parent
#         if os.name == 'nt':  # Windows
#             # Use CREATE_NEW_PROCESS_GROUP to make it independent
#             subprocess.Popen([sys.executable, script_path], 
#                            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.CREATE_NEW_CONSOLE,
#                            stdin=subprocess.DEVNULL,
#                            stdout=subprocess.DEVNULL,
#                            stderr=subprocess.DEVNULL)
#         else:  # Linux/Mac
#             # Use nohup-like approach to make process independent
#             subprocess.Popen([sys.executable, script_path], 
#                            stdin=subprocess.DEVNULL,
#                            stdout=subprocess.DEVNULL,
#                            stderr=subprocess.DEVNULL,
#                            start_new_session=True)  # This makes it independent
        
#         print("[SUCCESS] Background monitoring process started!")
#         return True
#     except Exception as e:
#         print(f"[ERROR] Failed to start background process: {e}")
#         return False

# # ---- SCRAPER ----
# def get_price_from_amazon(url: str):
#     options = Options()
#     options.add_argument("--headless=new")
#     options.add_argument("--no-sandbox")
#     options.add_argument("--disable-dev-shm-usage")
#     options.add_argument("--disable-blink-features=AutomationControlled")
#     options.add_experimental_option("excludeSwitches", ["enable-automation"])
#     options.add_experimental_option("useAutomationExtension", False)

#     driver = webdriver.Chrome(options=options)
#     try:
#         driver.get(url)
#         time.sleep(3)

#         price_selectors = [
#             "//span[@class='a-price-whole']",
#             "//span[contains(@class, 'a-price-whole')]",
#             "//span[@class='a-offscreen']"
#         ]
#         for selector in price_selectors:
#             try:
#                 price_elem = driver.find_element(By.XPATH, selector)
#                 price_text = price_elem.text.replace(",", "").replace("₹", "").replace("Rs.", "").strip()
#                 if price_text and price_text.replace('.', '', 1).isdigit():
#                     return int(float(price_text))
#             except:
#                 continue
#         return None
#     finally:
#         driver.quit()

# # ---- EMAIL ----
# def send_email(to_email: str, subject: str, body: str):
#     msg = MIMEMultipart()
#     msg['From'] = SENDER_EMAIL
#     msg['To'] = to_email
#     msg['Subject'] = subject
#     msg.attach(MIMEText(body, 'plain'))

#     try:
#         server = smtplib.SMTP('smtp.gmail.com', 587)
#         server.starttls()
#         server.login(SENDER_EMAIL, SENDER_PASSWORD)
#         server.sendmail(SENDER_EMAIL, to_email, msg.as_string())
#         server.quit()
#         print(f"[SUCCESS] Email sent to {to_email}")
#         return True
#     except Exception as e:
#         print(f"[ERROR] Failed to send email: {e}")
#         return False

# def send_confirmation_email(url, target_price):
#     subject = "[ALERT] Price Drop Alert Activated!"
#     body = f"""
#     You've asked us to watch this product on Amazon:

#     Product URL: {url}
#     Target Price: Rs.{target_price}

#     We'll notify you once it drops below the target price. Happy shopping!
    
#     Note: Monitoring will continue in the background even if you close the terminal.
#     """
#     print("[INFO] Sending confirmation email...")
#     return send_email(RECIPIENT_EMAIL, subject, body)

# # ---- CHECKER ----
# def check_price_and_notify(url: str, target_price: int = DEFAULT_TARGET_PRICE):
#     print(f"[CHECK] Checking price for: {url} at {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
#     try:
#         current_price = get_price_from_amazon(url)

#         if current_price is None:
#             print("[WARNING] Price not found.")
#             send_email(
#                 RECIPIENT_EMAIL,
#                 "[ERROR] Amazon Price Check Failed",
#                 f"We were unable to retrieve the price for:\n{url}\nWe'll retry during the next scheduled check.\n\nTime: {time.strftime('%Y-%m-%d %H:%M:%S')}"
#             )
#             return

#         print(f"[PRICE] Current price: Rs.{current_price} | Target: Rs.{target_price}")
        
#         # Update status
#         update_monitor_status("checking")
        
#         if current_price <= target_price:
#             subject = "[ALERT] Amazon Price Drop Alert!"
#             body = f"""
#             Good news! The price for your watched product has dropped!

#             Product URL: {url}
#             Current Price: Rs.{current_price}
#             Target Price: Rs.{target_price}
            
#             Time: {time.strftime('%Y-%m-%d %H:%M:%S')}

#             Hurry before it's gone!
#             """
#             send_email(RECIPIENT_EMAIL, subject, body)
#         else:
#             subject = "[UPDATE] Amazon Daily Price Check Update"
#             body = f"""
#             Scheduled price check completed.

#             Product URL: {url}
#             Current Price: Rs.{current_price}
#             Target Price: Rs.{target_price}
            
#             Time: {time.strftime('%Y-%m-%d %H:%M:%S')}

#             No drop yet. We'll continue monitoring and update you in the next check.
#             """
#             send_email(RECIPIENT_EMAIL, subject, body)
            
#     except Exception as e:
#         print(f"[ERROR] Error during price check: {e}")
#         send_email(
#             RECIPIENT_EMAIL,
#             "[ERROR] Amazon Price Check Error",
#             f"An error occurred while checking the price:\n{str(e)}\n\nURL: {url}\nTime: {time.strftime('%Y-%m-%d %H:%M:%S')}"
#         )

# # ---- ADDITIONAL UTILITY FUNCTIONS ----
# def stop_background_monitoring():
#     """Stop background monitoring process"""
#     try:
#         if os.name == 'nt':  # Windows
#             subprocess.run(['taskkill', '/F', '/IM', 'python.exe', '/FI', 'WINDOWTITLE eq background_monitor*'], 
#                          capture_output=True)
#         else:  # Linux/Mac
#             subprocess.run(['pkill', '-f', 'background_monitor.py'], capture_output=True)
        
#         # Update status
#         update_monitor_status("stopped")
#         print("[INFO] Background monitoring stopped.")
#         return True
#     except Exception as e:
#         print(f"[ERROR] Failed to stop background monitoring: {e}")
#         return False

# def get_background_process_status():
#     """Check if background process is running"""
#     try:
#         if os.name == 'nt':  # Windows
#             result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq python.exe'], 
#                                   capture_output=True, text=True)
#             return 'python.exe' in result.stdout
#         else:  # Linux/Mac
#             result = subprocess.run(['pgrep', '-f', 'background_monitor.py'], 
#                                   capture_output=True, text=True)
#             return bool(result.stdout.strip())
#     except Exception:
#         return False

# def schedule_daily_price_check(url, target_price, interval_seconds=120):
#     """
#     Start monitoring with background persistence
#     """
#     global running
    
#     # Check if there's already an active monitor
#     existing_config = check_monitor_status()
#     if existing_config and existing_config.get('status') in ['active', 'background_active']:
#         print("[WARNING] There's already an active monitor running.")
#         print("[INFO] Stopping existing monitor and starting new one...")
    
#     print("[START] Starting Amazon Price Monitor with Background Persistence...")
#     print(f"[INFO] Monitoring URL: {url}")
#     print(f"[INFO] Target Price: Rs.{target_price}")
#     print(f"[INFO] Check Interval: {interval_seconds} seconds")
    
#     # Save configuration for persistence
#     save_monitor_config(url, target_price, interval_seconds)
    
#     # Send confirmation email
#     confirmation_sent = send_confirmation_email(url, target_price)
    
#     if confirmation_sent:
#         print("[SUCCESS] Confirmation email sent successfully!")
#     else:
#         print("[WARNING] Failed to send confirmation email, but continuing monitoring...")
    
#     # Create and start background process

#     script_path = create_service_script(url, target_price, interval_seconds)
#     if start_background_process(script_path):
#         print("[SUCCESS] Background monitoring started successfully!")
#         print("[INFO] You'll receive email notifications for price changes.")
#         print("[INFO] Monitor will continue running in the background.")
#         print("[INFO] You can now press Ctrl+C to exit the foreground session.")
#         print("[INFO] The background monitoring will keep running independently.")
        
#         # Give some time for the background process to start
#         time.sleep(2)
        
#         # Keep the foreground session alive until user decides to exit
#         print("\n[WAIT] Foreground session active. Press Ctrl+C to exit (background will continue)...")
        
#         # Calculate end time (20 days from now)
#         start_time = datetime.now()
#         end_time = start_time + timedelta(days=20)
        
#         try:
#             while running and datetime.now() < end_time:
#                 # Call the price check function
#                 try:
#                     result = check_price_and_notify(url, target_price)
#                     print(f"[INFO] Price check completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                    
#                     # Check if target price was reached (assuming the function returns this info)
#                     # You might need to modify check_price_and_notify to return price status
#                     if "target price reached" in str(result).lower() or "price dropped" in str(result).lower():
#                         print("[SUCCESS] Target price reached! Exiting foreground session.")
#                         break
                        
#                 except Exception as e:
#                     print(f"[ERROR] Error during price check: {e}")
                
#                 # Wait for the specified interval before next check
#                 time.sleep(interval_seconds)
                
#         except KeyboardInterrupt:
#             # This will be handled by the signal handler
#             pass
        
#         # Check if we completed 20 days or exited early
#         if datetime.now() >= end_time:
#             print("[INFO] 20-day monitoring period completed. Exiting foreground session.")
        
#         return f"[SUCCESS] Price monitoring activated for {url}. Target: Rs.{target_price}"
        
#     else:
#         print("[WARNING] Failed to start background mode. Starting inline monitoring...")
        
#         # Fallback to inline monitoring (single check)
#         try:
#             check_price_and_notify(url, target_price)
#             return f"[SUCCESS] Price check completed for {url}. Email notification sent."
#         except Exception as e:
#             error_msg = f"[ERROR] Error during price check: {e}"
#             print(error_msg)
#             return error_msg

#     # ---- MAIN EXECUTION ----











import json
from pathlib import Path
from backend.utils.price_alert_utils import get_price_from_amazon, send_price_alert_email

PRODUCTS_FILE = Path("backend/utils/monitored_products.json")

def schedule_daily_price_check(url: str, target_price: int, user_id: int):
    PRODUCTS_FILE.parent.mkdir(parents=True, exist_ok=True)

    if PRODUCTS_FILE.exists():
        with open(PRODUCTS_FILE, "r") as f:
            products = json.load(f)
    else:
        products = []

    # Check current price and send email if condition met
    try:
        current_price = get_price_from_amazon(url)
        print(f"Current price: ₹{current_price}")

        if current_price <= target_price:
            price_dropped = True
            send_price_alert_email(url, current_price, target_price, price_dropped)
            print("✅ Email alert sent!")
        else:
            price_dropped = False
            send_price_alert_email(url, current_price, target_price, price_dropped)
            print("🔕 Price not low enough yet.")
    except Exception as e:
        print(f"❌ Failed to fetch price: {e}")
        return

    # Save or update the product in monitored_products.json
    found = False
    for p in products:
        if p["url"] == url:
            p["target_price"] = target_price
            found = True
            break

    if not found:
        products.append({"url": url, "target_price": target_price})

    with open(PRODUCTS_FILE, "w") as f:
        json.dump(products, f, indent=2)







