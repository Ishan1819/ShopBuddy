# bots/buy_now_bot.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time

def create_driver(headless=False):
    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=options)

def proceed_to_checkout(name, phone, address, payment_choice):
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

    # Step 2: Try to autofill address if needed
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        try:
            name_field = driver.find_element(By.ID, "address-ui-widgets-enterAddressFullName")
            print("📬 No address found. Autofilling details...")

            name_field.send_keys(name)
            driver.find_element(By.ID, "address-ui-widgets-enterAddressPhoneNumber").send_keys(phone)
            driver.find_element(By.ID, "address-ui-widgets-enterAddressLine1").send_keys(address)
            driver.find_element(By.XPATH, "//input[@type='submit']").click()
            print("✅ Address submitted.")

        except NoSuchElementException:
            print("✅ Address already present or form not shown.")
    except Exception as e:
        print("🟠 Unexpected issue during address detection:", str(e))

    time.sleep(5)
    print(f"💳 Selected payment option: {payment_choice}")

    # Step 3: Handle payment method
    if not payment_choice:
        driver.quit()
        return "❌ No payment option selected."

    if payment_choice in [1, 2, 3, 4]:
        print("🔗 Redirecting to Amazon's official payment gateway...")
        input("🛑 Please complete the payment in the opened browser. Press ENTER to close the browser...")
        driver.quit()
        return "✅ Please complete the payment on Amazon's official site."

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
            print(f"🛍️ Product to be booked: {product_url}")
            confirm_button.click()

            print("🎉 Order placed successfully via COD!")
            driver.quit()
            return f"🛒 Booked successfully!\n🔗 Product URL: {product_url}"

        except Exception as e:
            driver.quit()
            return f"❌ COD flow failed: {e}"

    else:
        driver.quit()
        return "❌ Invalid payment option."
