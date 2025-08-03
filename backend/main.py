# import os
# import re
# import json
# import sys
# import dotenv
# import uvicorn
# import tempfile
# import speech_recognition as sr
# import google.generativeai as genai
# from fastapi import FastAPI, Request, UploadFile, File
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi import APIRouter, HTTPException
# from fastapi.responses import JSONResponse
# import os
# import json

# router = APIRouter()
# # Add project root to path
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# from backend.crew_config.crew_setup import (
#     create_parser_search_crew,
#     create_addtocart_crew,
#     create_price_drop_crew,
#     create_buy_now_crew
# )

# # -----------------------------
# # Load environment and configure Gemini
# # -----------------------------
# dotenv.load_dotenv()
# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
# model = genai.GenerativeModel("gemini-1.5-flash")

# # -----------------------------
# # Gemini command classification
# # -----------------------------
# def route_command(query):
#     prompt = f"""
# You are an AI assistant for a shopping assistant app. Based on the user command below, return a JSON object like this:
# {{
#   "action": "<one of: search_products, add_to_cart, price_notifier, buy_now, exit, or unknown>",
#   "query": "<original or modified user query if needed>"
# }}

# Only return the JSON. Do not include explanations.

# User command: "{query}"
# """
#     response = model.generate_content(prompt)
#     raw_text = response.text.strip()
#     print("📨 Gemini raw response:", raw_text)

#     cleaned = re.sub(r"^```(?:json)?", "", raw_text)
#     cleaned = re.sub(r"```$", "", cleaned).strip()

#     try:
#         return json.loads(cleaned)
#     except Exception as e:
#         print("❌ Failed to parse Gemini response:", e)
#         return {"action": "unknown", "query": query}

# # -----------------------------
# # Gemini transcription from audio
# # -----------------------------
# def gemini_transcribe(audio_file_path):
#     with open(audio_file_path, "rb") as audio_file:
#         response = model.generate_content(
#             contents=[
#                 "You are a helpful AI that transcribes user voice commands into plain text queries.",
#                 {"mime_type": "audio/webm", "data": audio_file.read()}
#             ]
#         )
#         return response.text.strip()

# # -----------------------------
# # Voice input helper (for CLI testing)
# # -----------------------------
# def get_voice_input():
#     recognizer = sr.Recognizer()
#     mic = sr.Microphone()
#     with mic as source:
#         print("🎙️ Speak your query...")
#         recognizer.adjust_for_ambient_noise(source)
#         audio = recognizer.listen(source)
#     try:
#         text = recognizer.recognize_google(audio)
#         print("🗣️ You said:", text)
#         return text
#     except sr.UnknownValueError:
#         print("❌ Could not understand audio.")
#         return None

# # -----------------------------
# # CLI flows (optional for testing)
# # -----------------------------
# def search_products_flow(user_query=None):
#     if not user_query:
#         user_query = input("🔍 What do you want to search? ").strip()
#     if not user_query:
#         print("⚠️ No query entered.")
#         return

#     parser_search_crew = create_parser_search_crew(user_query)
#     parser_search_crew.kickoff()
#     task_output = parser_search_crew.tasks[1].output

#     try:
#         if isinstance(task_output, str):
#             search_results = json.loads(task_output)
#         elif isinstance(task_output, dict):
#             search_results = task_output
#         elif hasattr(task_output, "model_dump"):
#             search_results = task_output.model_dump().get("output", [])
#         else:
#             raise ValueError("❌ Unsupported output format.")
#     except Exception as e:
#         print(f"❌ Failed to parse product list: {e}")
#         return

#     if not isinstance(search_results, list):
#         print("❌ Unexpected format of search results.")
#         return

#     print("\n🛍️ Top 15 Products:\n")
#     for idx, product in enumerate(search_results, 1):
#         print(f"{idx}. {product['title'][:60]}...\n   💰 {product.get('price', 'N/A')} | 🔗 {product['url']}\n")

# def add_to_cart_flow():
#     url = input("🛒 Enter the product URL to add to cart: ").strip()
#     if url:
#         cart_crew = create_addtocart_crew(url)
#         cart_crew.kickoff()

# def price_notifier_flow():
#     url = input("🔔 Enter the product URL for price drop notifications: ").strip()
#     if url:
#         price_drop_crew = create_price_drop_crew(url)
#         price_drop_crew.kickoff()

# def buy_now_flow():
#     print("💳 Proceeding to buy now...")
#     buy_crew = create_buy_now_crew()
#     buy_crew.kickoff()

# # -----------------------------
# # Optional voice loop (for terminal testing)
# # -----------------------------
# def voice_assistant_loop():
#     print("🛒 Welcome to ShopBuddyAI with Voice Assistant!")

#     while True:
#         print("🗣️ Say 'start' to give a command or 'exit' to quit.")
#         # command_trigger = get_voice_input()

#         # if not command_trigger:
#         #     continue

#         # if "exit" in command_trigger.lower():
#         #     print("👋 Exiting ShopBuddyAI. See you again!")
#         #     break

#         # if "start" not in command_trigger.lower():
#         #     print("❗ Please say 'start' to begin or 'exit' to quit.")
#         #     continue

#         # print("🎙️ Speak your command (e.g., find me Nike shoes)...")
#         query = input("Type your command: ").strip()
#         if not query:
#             print("❌ Could not understand your query.")
#             continue

#         result = route_command(query)
#         action = result.get("action", "unknown")
#         extracted_query = result.get("query", "")

#         print("🤖 Gemini action:", action)
#         print("🗣️ Interpreted query:", extracted_query)

#         if action == "search_products":
#             search_products_flow(extracted_query)
#         elif action == "add_to_cart":
#             add_to_cart_flow()
#         elif action == "price_notifier":
#             price_notifier_flow()
#         # elif action == "buy_now":
#         #     buy_now_flow()
#         elif action == "exit":
#             print("👋 Exiting ShopBuddyAI. See you again!")
#             break
#         else:
#             print("❌ Sorry, I can help with only search_products, add_to_cart, price_notifier, or exit.")

# -----------------------------
# FastAPI App
# -----------------------------
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from fastapi.staticfiles import StaticFiles
import os
from router import router  # importing your APIRouter instance
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()

# Secret key for signing cookies (keep it secret!)
app.add_middleware(SessionMiddleware, secret_key="supersecret-key")
# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root path
# @app.get("/")
# def root():
#     return {"message": "Welcome to ShopBuddyAI! Use the /api/query or /api/products endpoints."}

# Include all APIs under /api
app.include_router(router, prefix="/api")
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
print("📁 Serving frontend from:", frontend_path)
print("📄 index.html exists:", os.path.exists(os.path.join(frontend_path, "index.html")))

app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
# -----------------------------
# Entry point
# -----------------------------
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
