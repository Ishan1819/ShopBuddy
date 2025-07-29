# import os
# import re
# import json
# import google.generativeai as genai
# from dotenv import load_dotenv

# load_dotenv()
# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# def parse_address_with_gemini(name, phone, full_address):
#     prompt = f"""
# You are a professional form assistant. Given the following delivery details, extract only the values required for Amazon's delivery form.

# Return output as pure JSON only, with no markdown or explanation.

# Input:
# Full Name: {name}
# Phone Number: {phone}
# Full Address: {full_address}

# Output Format:
# {{
#   "pincode": "",
#   "flat": "",
#   "street": "",
#   "landmark": "",
#   "city": "",
#   "state": ""
# }}
# """
#     model = genai.GenerativeModel("gemini-1.5-flash")
#     response = model.generate_content(prompt)
#     raw_text = response.text.strip()

#     if raw_text.startswith("```"):
#         raw_text = re.sub(r"```(?:json)?", "", raw_text).strip()
#         raw_text = re.sub(r"```", "", raw_text).strip()

#     try:
#         return json.loads(raw_text)
#     except Exception as e:
#         print("❌ Failed to parse Gemini response:", e)
#         return {}
