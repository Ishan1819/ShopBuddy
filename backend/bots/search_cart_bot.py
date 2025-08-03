import pymysql
import os
import re
import json
from datetime import datetime
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment and configure Gemini
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

def extract_title_and_time(query: str):
    """
    Uses Gemini to extract product title and time range from user query.
    Returns: (product_description: str, (start_datetime, end_datetime) or None)
    """

    prompt = f"""
You are a smart shopping assistant.
Extract the product title and time range (if any) from this query.

Respond ONLY in this JSON format:
{{
  "product_description": "protein powder",
  "time_range": {{
    "start": "2024-06-01T00:00:00",
    "end": "2024-06-30T23:59:59"
  }}
}}

If no time is mentioned, use:
"time_range": null

User query: "{query}"
Return only the JSON. No explanation or formatting.
    """

    try:
        response = model.generate_content(prompt)
        content = response.text.strip()

        # Clean if markdown formatting present
        if content.startswith("```"):
            content = re.sub(r"```[a-zA-Z]*\n", "", content)
            content = content.replace("```", "").strip()

        data = json.loads(content)

        product_description = data.get("product_description", "").strip()
        time_range = data.get("time_range")

        if time_range:
            start = datetime.fromisoformat(time_range["start"])
            end = datetime.fromisoformat(time_range["end"])
            return product_description, (start, end)
        else:
            return product_description, None

    except Exception as e:
        print("⚠️ Error extracting with Gemini:", e)
        return query.strip(), None  # fallback if parsing fails


# backend/utils/search_cart_items.py

def search_products(query: str, user_id: str):
    # from backend.utils.time_extractor import extract_title_and_time  # if needed

    title_query, time_range = extract_title_and_time(query)

    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="12345",
        database="shopbuddy",
        cursorclass=pymysql.cursors.DictCursor
    )
    cursor = conn.cursor()

    sql = "SELECT * FROM cartadders WHERE user_id = %s AND product_description LIKE %s"
    params = [user_id, f"%{title_query}%"]

    if time_range:
        sql += " AND timestamp BETWEEN %s AND %s"
        params += [time_range[0], time_range[1]]

    cursor.execute(sql, tuple(params))
    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return results
