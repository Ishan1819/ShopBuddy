import os
import time
import json
import google.generativeai as genai
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import json
import re



# Load API key from .env
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

import undetected_chromedriver as uc  # NEW: Install via pip

def create_driver(headless=True):
    options = uc.ChromeOptions()
    if headless:
        options.add_argument("--headless=new")

    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-gpu"    )
    options.add_argument("--disable-infobars")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-extensions")

    # Use a real user-agent
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.76")


    # Launch undetected driver
    driver = uc.Chrome(options=options)


    # Bypass navigator.webdriver = true
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })

    return driver



def parse_address_with_gemini(name, phone, full_address):
    prompt = f"""
You are a professional form assistant. Given the following delivery details, extract only the values required for Amazon's delivery form.

Return output as pure JSON only, with no markdown or explanation.

Input:
Full Name: {name}
Phone Number: {phone}
Full Address: {full_address}

Output Format:
{{
  "pincode": "",
  "flat": "",
  "street": "",
  "landmark": "",
  "city": "",
  "state": ""
}}
"""
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)

    raw_text = response.text.strip()
    print("📨 Raw Gemini response:", raw_text)

    # Remove markdown code block if present
    if raw_text.startswith("```json") or raw_text.startswith("```"):
        raw_text = re.sub(r"```(?:json)?", "", raw_text).strip()
        raw_text = re.sub(r"```", "", raw_text).strip()

    try:
        return json.loads(raw_text)
    except Exception as e:
        print("❌ Failed to parse cleaned response:", e)
        return {}



def proceed_to_checkout(payment_choice):
    # Step 1: Use headless driver to get final checkout URL
    headless_driver = create_driver(headless=True)
    headless_driver.get("https://www.amazon.in/gp/cart/view.html")
    time.sleep(3)
    # Step 0: Check and perform login if needed
    try:
        # Check if redirected to sign-in
        if "signin" in headless_driver.current_url:
            print("🔐 Signing in...")

            email_input = WebDriverWait(headless_driver, 10).until(
                EC.presence_of_element_located((By.ID, "ap_email"))
            )
            email_input.send_keys(os.getenv("AMAZON_EMAIL"))
            headless_driver.find_element(By.ID, "continue").click()

            password_input = WebDriverWait(headless_driver, 10).until(
                EC.presence_of_element_located((By.ID, "ap_password"))
            )
            password_input.send_keys(os.getenv("AMAZON_PASSWORD"))
            headless_driver.find_element(By.ID, "signInSubmit").click()

            print("✅ Signed in successfully.")

            # Optional: wait for the cart to reload
            WebDriverWait(headless_driver, 10).until(
                EC.presence_of_element_located((By.ID, "sc-active-cart"))
            )

    except Exception as e:
        print(f"❌ Sign-in failed: {e}")
        headless_driver.quit()
        return

    try:
        name = input("👤 Enter your full name: ")
        phone = input("📞 Enter your phone number: ")
        full_address = input("🏠 Enter your full delivery address (everything): ")
        
        proceed_button = headless_driver.find_element(By.NAME, "proceedToRetailCheckout")
        proceed_button.click()
        print("👉 Proceeded to checkout in headless mode...")
        
        # Wait until page loads after proceed
        WebDriverWait(headless_driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        final_url = headless_driver.current_url
        print(f"🌐 Extracted payment URL: {final_url}")

    except Exception as e:
        headless_driver.quit()
        return f"❌ Error while getting payment page URL: {e}"

    headless_driver.quit()

    # Step 2: Launch visible driver and go to the payment page directly
    driver = create_driver(headless=True)
    driver.get(final_url)
    time.sleep(5)

    # Step 3: Handle address input if necessary
    try:
        if "select-address" not in driver.current_url:
            print("ℹ️ No saved address found. Asking user for input...")
            parsed = parse_address_with_gemini(name, phone, full_address)
            print("📦 Parsed Address from Gemini:", parsed)

            driver.find_element(By.NAME, "address-ui-widgets-enterAddressFullName").send_keys(name)
            driver.find_element(By.NAME, "address-ui-widgets-enterAddressPhoneNumber").send_keys(phone)
            driver.find_element(By.NAME, "address-ui-widgets-enterAddressPostalCode").send_keys(parsed.get("pincode", ""))
            driver.find_element(By.NAME, "address-ui-widgets-enterAddressLine1").send_keys(parsed.get("flat", ""))
            driver.find_element(By.NAME, "address-ui-widgets-enterAddressLine2").send_keys(parsed.get("street", ""))
            driver.find_element(By.NAME, "address-ui-widgets-landmark").send_keys(parsed.get("landmark", ""))
            driver.find_element(By.NAME, "address-ui-widgets-enterAddressCity").send_keys(parsed.get("city", ""))
            driver.find_element(By.NAME, "address-ui-widgets-enterAddressStateOrRegion").send_keys(parsed.get("state", ""))

            input("👀 Review and press ENTER to submit the address...")
            driver.find_element(By.XPATH, "//input[@type='submit']").click()
            print("✅ Address submitted.")
        else:
            print("✅ Existing address found, skipping input.")
    except Exception as e:
        print("⚠️ Address autofill skipped due to error:", e)

    time.sleep(5)

    # Step 4: Payment method handling
    print(f"💳 Selected payment option: {payment_choice}")
    if not payment_choice:
        driver.quit()
        return "❌ No payment option selected."

    if payment_choice in [1, 2, 3, 4]:
        input("💳 Complete payment manually in the browser and press ENTER to close...")
        driver.quit()
        return "✅ Manual payment initiated."

    elif payment_choice == 5:
        try:
            cod_button = driver.find_element(By.XPATH, "//input[@type='radio' and @value='COD']")
            cod_button.click()
            time.sleep(2)

            continue_button = driver.find_element(By.XPATH, "//input[@type='submit' and contains(@value, 'Continue')]")
            continue_button.click()
            time.sleep(3)

            confirm_button = driver.find_element(By.NAME, "placeYourOrder1")
            product_url = driver.current_url
            confirm_button.click()

            driver.quit()
            return f"🎉 Order placed via COD!\n🔗 URL: {product_url}"
        except Exception as e:
            driver.quit()
            return f"❌ COD flow failed: {e}"

    driver.quit()
    return "❌ Invalid payment option."

















# import time
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import NoSuchElementException

# from backend.utils.driver_factory import create_driver
# from backend.utils.gemini_parser import parse_address_with_gemini

# def proceed_to_checkout(payment_choice):
#     driver = create_driver()
#     driver.get("https://www.amazon.in/gp/cart/view.html")
#     time.sleep(3)

#     # Proceed to checkout
#     try:
#         driver.find_element(By.NAME, "proceedToRetailCheckout").click()
#         print("✅ Proceeded to checkout.")
#     except Exception as e:
#         driver.quit()
#         return f"❌ Could not click Proceed to Buy: {e}"

#     time.sleep(5)

#     # Check for existing delivery address
#     try:
#         if "select-address" in driver.current_url:
#             print("✅ Existing address found. Skipping input.")
#         else:
#             print("ℹ️ No saved address found. Asking user for address input.")
#             name = input("👤 Enter full name: ")
#             phone = input("📞 Enter phone number: ")
#             full_address = input("🏠 Enter full delivery address (everything): ")

#             parsed = parse_address_with_gemini(name, phone, full_address)
#             print("📦 Parsed Address:", parsed)

#             driver.find_element(By.NAME, "address-ui-widgets-enterAddressFullName").send_keys(name)
#             driver.find_element(By.NAME, "address-ui-widgets-enterAddressPhoneNumber").send_keys(phone)
#             driver.find_element(By.NAME, "address-ui-widgets-enterAddressPostalCode").send_keys(parsed.get("pincode", ""))
#             driver.find_element(By.NAME, "address-ui-widgets-enterAddressLine1").send_keys(parsed.get("flat", ""))
#             driver.find_element(By.NAME, "address-ui-widgets-enterAddressLine2").send_keys(parsed.get("street", ""))
#             driver.find_element(By.NAME, "address-ui-widgets-landmark").send_keys(parsed.get("landmark", ""))
#             driver.find_element(By.NAME, "address-ui-widgets-enterAddressCity").send_keys(parsed.get("city", ""))
#             driver.find_element(By.NAME, "address-ui-widgets-enterAddressStateOrRegion").send_keys(parsed.get("state", ""))

#             input("👀 Review address in browser and press ENTER to submit...")
#             driver.find_element(By.XPATH, "//input[@type='submit']").click()
#             print("✅ Address submitted.")
#     except Exception as e:
#         print("⚠️ Issue during address handling:", e)

#     time.sleep(5)
#     print(f"💳 Selected payment option: {payment_choice}")

#     if not payment_choice:
#         driver.quit()
#         return "❌ No payment option selected."

#     if payment_choice in [1, 2, 3, 4]:
#         input("💳 Complete payment manually and press ENTER to close browser...")
#         driver.quit()
#         return "✅ Payment manually initiated."

#     elif payment_choice == 5:
#         try:
#             cod_btn = driver.find_element(By.XPATH, "//input[@type='radio' and @value='COD']")
#             cod_btn.click()
#             driver.find_element(By.XPATH, "//input[@type='submit']").click()
#             time.sleep(3)
#             driver.find_element(By.NAME, "placeYourOrder1").click()
#             print("🎉 COD order placed!")
#             driver.quit()
#             return "✅ Order placed using COD!"
#         except Exception as e:
#             driver.quit()
#             return f"❌ COD flow failed: {e}"

#     driver.quit()
#     return "❌ Invalid payment option."
