# backend/nlp/parser.py

import os
import re
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

def parse_user_query_with_gemini(query: str) -> dict:
    prompt = f"""
You are a smart shopping assistant. 
Extract structured information from the user's request and return it in JSON format.

If something is not mentioned, fill with "any" or defaults.
JSON Format:
{{
  "platform": ["amazon", "flipkart", "myntra", "any"],  # <-- Make this a list
  "category": "t-shirt, shoes, jeans, washing machine, etc.",
  "brand": "brand name or any",
  "gender": "men, women, unisex, kids, or any",
  "color": "color or any",
  "material": "if mentioned like cotton, leather, denim or any",
  "min_price": 0,
  "max_price": 999999,
  "min_rating": 0.0
}}

User Query: "{query}"
Return only the JSON.
"""

    response = model.generate_content(prompt)
    try:
        content = response.text.strip()

        # Remove markdown code block if present
        if content.startswith("```"):
            content = re.sub(r"```[a-zA-Z]*\n", "", content)
            content = content.replace("```", "").strip()

        parsed = eval(content)  # Use json.loads() if you want stricter parsing
        return parsed
    except Exception as e:
        print("Parsing error:", e)
        return {"error": "Could not parse response", "raw_output": response.text}
