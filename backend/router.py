from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import json
import os
from fastapi import APIRouter, Form, Request, Response
# from bots.login_bot import login_signup
import mysql.connector
from test_main import route_command, create_parser_search_crew, add_to_cart_flow, create_login_crew, search_products_flow, get_cart_history_flow
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
router = APIRouter()

# ---------- POST: /api/query ----------
class QueryInput(BaseModel):
    query: str
    
class CartRequest(BaseModel):
    url: str

# @router.post("/add_to_cart", tags=["Cart"])
# async def add_to_cart(payload: CartRequest):
#     url = payload.url.strip()
#     if not url:
#         return {"error": "No URL provided."}

#     try:
#         add_to_cart_flow(url)
#         # cart_crew.kickoff()
#         return {"message": "Product added to cart successfully"}
#     except Exception as e:
#         return {"error": f"Cart error: {str(e)}"}


@router.post("/add-to-cart", tags=["Cart"])
async def add_to_cart_endpoint(request: Request, product_url: str):
    try:
        # Get user_id from cookies
        user_id = request.cookies.get("user_id")
        
        if not user_id:
            return JSONResponse(
                status_code=401,
                content={
                    "status": "error",
                    "message": "User not authenticated. Please login first."
                }
            )
        
        # Convert user_id to int
        user_id = int(user_id)
        
        print(f"🛒 Cart request - URL: {product_url}, User ID: {user_id}")
        
        # Call the cart flow with user_id
        result = add_to_cart_flow(product_url, user_id)
        
        return {
            "status": "success",
            "message": result,
            "user_id": user_id
        }
        
    except ValueError:
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "message": "Invalid user ID format"
            }
        )
    except Exception as e:
        print(f"❌ Cart endpoint error: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": f"Internal server error: {str(e)}"
            }
        )




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


# from fastapi import APIRouter, Request, Response, Form
# from fastapi.responses import JSONResponse

@router.post("/login", tags=["Auth"])
async def login(response: Response, email: str, password: str):
    try:
        # Step 1: Call Crew to handle login/signup logic
        print("🔍 About to call create_login_crew...")
        crew_result = await create_login_crew(email=email, password=password)
        print("🔍 After await - crew_result:", crew_result)
        print("🔍 crew_result type:", type(crew_result))
        
        # Step 2: Extract result data from CrewOutput
        if hasattr(crew_result, 'raw'):
            # Parse the raw string result
            import json
            try:
                result = json.loads(crew_result.raw)
                print("🔧 Parsed from raw:", result)
            except json.JSONDecodeError:
                # If it's not valid JSON, try to evaluate as Python literal
                import ast
                result = ast.literal_eval(crew_result.raw)
                print("🔧 Parsed from literal_eval:", result)
        elif hasattr(crew_result, "output"):
            result = json.loads(crew_result.output)
        elif hasattr(crew_result, "to_dict"):
            result = crew_result.to_dict()
        elif isinstance(crew_result, dict):
            result = crew_result
        else:
            raise ValueError(f"Unexpected crew result format. Type: {type(crew_result)}")

        print("🔧 Final parsed result:", result)
        print("🔧 Final parsed result type:", type(result))

        # Step 3: Process login/signup success
        if isinstance(result, dict) and result.get("status") in ["signed_in", "signed_up"]:
            print("✅ ENTERING SUCCESS BLOCK")
            response.set_cookie(
                key="user_id",
                value=str(result["user_id"]),
                httponly=True,
                samesite="Lax",
                secure=False
            )
            print("User ID set in cookie:", result["user_id"])
            print("Login/Signup successful:", result)
            return {
                "status": result["status"],
                "message": result["message"],
                "user_id": result["user_id"]
            }
        else:
            print("❌ NOT ENTERING SUCCESS BLOCK")
            print("❌ isinstance(result, dict):", isinstance(result, dict))
            if isinstance(result, dict):
                print("❌ result.get('status'):", repr(result.get("status")))
                print("❌ Expected values:", ["signed_in", "signed_up"])

        # Step 4: Handle failure cases
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "message": result.get("message", "Login/Signup failed.") if isinstance(result, dict) else "Login/Signup failed."
            }
        )

    except Exception as e:
        print("❌ Exception in login:", e)
        print("❌ Exception type:", type(e))
        import traceback
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": f"Internal server error: {str(e)}"
            }
        )



@router.post("/cart/search", tags=["Cart"])
async def search_cart(request: Request, query: str = Form(...)):
    user_id = request.cookies.get("user_id")

    if not user_id:
        return {"error": "User not authenticated"}

    cart_items = search_products_flow(query, user_id)
    print(cart_items)
    print(type(cart_items))
    return {
        "user_id": user_id,
        "search_query": query,
        "cart_items": cart_items
    }
    
    
@router.get("/login")
def login_redirect():
    return RedirectResponse(url="/")



# class CartHistoryRequest(BaseModel):
#     query: str  # User's search query like "shoes", "bags", "handbags I added yesterday"

# @router.post("/cart-history", tags=["Cart"])
# async def get_cart_history_endpoint(request: Request, search_request: CartHistoryRequest):
#     try:
#         # Get user_id from cookies
#         user_id = request.cookies.get("user_id")
        
#         if not user_id:
#             return JSONResponse(
#                 status_code=401,
#                 content={
#                     "status": "error",
#                     "message": "User not authenticated. Please login first."
#                 }
#             )
        
#         user_id = int(user_id)
#         query = search_request.query
        
#         print(f"📚 Cart history search for user: {user_id}, query: '{query}'")
        
#         # Call the cart history flow with search query
#         result = get_cart_history_flow(user_id, query)
        
#         return {
#             "status": "success",
#             "data": result,
#             "user_id": user_id,
#             "search_query": query
#         }
        
#     except ValueError:
#         return JSONResponse(
#             status_code=400,
#             content={
#                 "status": "error",
#                 "message": "Invalid user ID format"
#             }
#         )
#     except Exception as e:
#         print(f"❌ Cart history endpoint error: {e}")
#         return JSONResponse(
#             status_code=500,
#             content={
#                 "status": "error",
#                 "message": f"Internal server error: {str(e)}"
#             }
#         )
