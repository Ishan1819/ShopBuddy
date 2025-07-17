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

def create_driver(headless=False):
    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=options)


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



def proceed_to_checkout(name, phone, full_address, payment_choice):
    driver = create_driver(headless=False)
    driver.get("https://www.amazon.in/gp/cart/view.html")
    time.sleep(3)

    # Step 1: Click Proceed to Buy
    try:
        proceed_button = driver.find_element(By.NAME, "proceedToRetailCheckout")
        proceed_button.click()
        print("👉 Proceeded to checkout.")
    except Exception as e:
        driver.quit()
        return f"❌ Could not click Proceed to Buy: {e}"

    time.sleep(5)

    # Step 2: Parse and autofill address
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        # ➕ Step 2a: Click "Add a new delivery address"
        try:
            print("🔍 Looking for 'Add a new address' button...")
            add_new_address_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((
                    By.XPATH, "//a[contains(text(), 'Add a new delivery address')] | //span[contains(text(), 'Add a new address')]"
                ))
            )
            print("➕ Clicking 'Add a new delivery address'...")
            add_new_address_btn.click()
            time.sleep(2)
        except Exception as e:
            print("⚠️ 'Add a new delivery address' button not found or already opened:", e)
            print("📄 Current page title:", driver.title)
            print("📄 Current URL:", driver.current_url)


        parsed = parse_address_with_gemini(name, phone, full_address)
        print("📦 Parsed address from Gemini:", parsed)

        try:
            driver.find_element(By.NAME, "address-ui-widgets-enterAddressFullName").send_keys(name)
            driver.find_element(By.NAME, "address-ui-widgets-enterAddressPhoneNumber").send_keys(phone)
            driver.find_element(By.NAME, "address-ui-widgets-enterAddressPostalCode").send_keys(parsed.get("pincode", ""))
            driver.find_element(By.NAME, "address-ui-widgets-enterAddressLine1").send_keys(parsed.get("flat", ""))
            driver.find_element(By.NAME, "address-ui-widgets-enterAddressLine2").send_keys(parsed.get("street", ""))
            driver.find_element(By.NAME, "address-ui-widgets-landmark").send_keys(parsed.get("landmark", ""))
            driver.find_element(By.NAME, "address-ui-widgets-enterAddressCity").send_keys(parsed.get("city", ""))
            driver.find_element(By.NAME, "address-ui-widgets-enterAddressStateOrRegion").send_keys(parsed.get("state", ""))

            print("👀 Please review the pre-filled address on the Amazon page. Once satisfied, press ENTER to continue...")
            input("✔️ Press ENTER to proceed with submission...")
            driver.find_element(By.XPATH, "//input[@type='submit']").click()
            print("✅ Address submitted.")
        except NoSuchElementException:
            print("✅ Address already present or form not shown.")
    except Exception as e:
        print("🟠 Unexpected issue during address autofill:", e)

    time.sleep(5)
    print(f"💳 Selected payment option: {payment_choice}")

    # Step 3: Payment Handling
    if not payment_choice:
        driver.quit()
        return "❌ No payment option selected."

    if payment_choice in [1, 2, 3, 4]:
        input("💳 Complete payment manually and press ENTER to close browser...")
        driver.quit()
        return "✅ Payment manually initiated."

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
    else:
        driver.quit()
        return "❌ Invalid payment option."