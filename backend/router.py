from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import json
import os

from test_main import route_command, create_parser_search_crew, add_to_cart_flow

router = APIRouter()

# ---------- POST: /api/query ----------
class QueryInput(BaseModel):
    query: str
    
class CartRequest(BaseModel):
    url: str

@router.post("/add_to_cart", tags=["Cart"])
async def add_to_cart(payload: CartRequest):
    url = payload.url.strip()
    if not url:
        return {"error": "No URL provided."}

    try:
        cart_crew = add_to_cart_flow(url)
        cart_crew.kickoff()
        return {"message": "Product added to cart successfully"}
    except Exception as e:
        return {"error": f"Cart error: {str(e)}"}

@router.post("/query", tags=["Query"])
async def handle_query(payload: QueryInput):
    query = payload.query

    if not query:
        return {"error": "No query provided."}

    result = route_command(query)
    action = result.get("action")
    refined_query = result.get("query")

    if action == "search_products":
        crew = create_parser_search_crew(refined_query)
        crew.kickoff()
        task_output = crew.tasks[1].output
        print("🔍 Search results:", task_output)

        try:
            if isinstance(task_output, list):
                return task_output
            elif isinstance(task_output, str):
                return json.loads(task_output)
            elif isinstance(task_output, dict):
                return [task_output]
            elif hasattr(task_output, "model_dump"):
                return task_output.model_dump().get("output", [])
            else:
                return {"error": "Unexpected output format"}
        except Exception as e:
            return {"error": f"Parsing error: {str(e)}"}

# ---------- GET: /api/products ----------
@router.get("/products", tags=["Products"])
def get_saved_products():
    file_path = "products.json"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="No product data found.")

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return JSONResponse(content=data)
