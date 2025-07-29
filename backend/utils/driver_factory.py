# import undetected_chromedriver as uc

# def create_driver(headless=True):
#     options = uc.ChromeOptions()
#     if headless:
#         options.add_argument("--headless=new")

#     options.add_argument("--no-sandbox")
#     options.add_argument("--disable-dev-shm-usage")
#     options.add_argument("--disable-blink-features=AutomationControlled")
#     options.add_argument("--disable-gpu")
#     options.add_argument("--disable-infobars")
#     options.add_argument("--window-size=1920,1080")
#     options.add_argument("--start-maximized")
#     options.add_argument("--disable-extensions")
#     options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")

#     driver = uc.Chrome(options=options)
    
#     # Prevent detection via navigator.webdriver
#     driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
#         "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
#     })

#     return driver
