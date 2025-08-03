import pymysql
from pymysql.err import MySQLError as Error
from pymysql.cursors import DictCursor
from dotenv import load_dotenv
from datetime import datetime, timedelta
import re
import os

load_dotenv()

def search_user_cart_history(user_id: int, search_query: str):
    """
    Search cart history for a specific user based on query
    
    Args:
        user_id: User ID to search for
        search_query: User's search query
        
    Returns:
        Dictionary with search results and metadata
    """
    conn = None
    try:
        conn = pymysql.connect(
            host="localhost",
            user="root",
            password="12345",
            database="shopbuddy",
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True,
            auth_plugin="mysql_native_password" 
        )
        cursor = conn.cursor()
        
        # Parse the search query to understand intent
        search_analysis = analyze_search_query(search_query)
        
        # Build the SQL query based on analysis
        sql_query, sql_params = build_search_query(user_id, search_analysis)
        
        print(f"🔍 Executing query: {sql_query}")
        print(f"🔍 Parameters: {sql_params}")
        
        cursor.execute(sql_query, sql_params)
        cart_items = cursor.fetchall()
        
        if not cart_items:
            return format_no_results_response(search_query, search_analysis)
        
        # Format and return results
        return format_search_results(cart_items, search_query, search_analysis)
        
    except Error as e:
        print(f"❌ Database error: {e}")
        return {
            "success": False,
            "message": f"❌ Sorry, I couldn't search your cart history due to a database error: {str(e)}",
            "items": []
        }
        
    finally:
        if conn and conn.open:
            cursor.close()
            conn.close()

def analyze_search_query(query: str):
    """Analyze user's search query to understand intent"""
    query_lower = query.lower()
    analysis = {
        "time_filter": None,
        "product_keywords": [],
        "time_range_hours": None,
        "original_query": query
    }
    
    # Time-based patterns
    time_patterns = {
        r'\b(\d+)\s*hours?\s*(ago|before|back)\b': lambda m: int(m.group(1)),
        r'\byesterday\b': lambda m: 24,
        r'\btoday\b': lambda m: 24,
        r'\blast\s*week\b': lambda m: 24 * 7,
        r'\blast\s*(\d+)\s*days?\b': lambda m: int(m.group(1)) * 24,
        r'\b(\d+)\s*days?\s*(ago|before|back)\b': lambda m: int(m.group(1)) * 24,
    }
    
    for pattern, calculator in time_patterns.items():
        match = re.search(pattern, query_lower)
        if match:
            analysis["time_range_hours"] = calculator(match)
            analysis["time_filter"] = match.group(0)
            break
    
    # Product keyword extraction
    # Remove time-related words and common words
    stop_words = {'i', 'add', 'added', 'to', 'cart', 'the', 'what', 'which', 'did', 
                  'hours', 'before', 'ago', 'yesterday', 'today', 'last', 'week', 'day', 'days'}
    
    words = re.findall(r'\b\w+\b', query_lower)
    product_keywords = [word for word in words if word not in stop_words and len(word) > 2]
    
    analysis["product_keywords"] = product_keywords
    
    return analysis

def build_search_query(user_id: int, analysis: dict):
    """Build SQL query based on search analysis"""
    base_query = """
    SELECT id, product_description, product_url, price, timestamp 
    FROM cartadders 
    WHERE user_id = %s
    """
    
    conditions = []
    params = [user_id]
    
    # Add time filter if specified
    if analysis["time_range_hours"]:
        time_threshold = datetime.now() - timedelta(hours=analysis["time_range_hours"])
        conditions.append("timestamp >= %s")
        params.append(time_threshold)
    
    # Add product keyword filters
    if analysis["product_keywords"]:
        keyword_conditions = []
        for keyword in analysis["product_keywords"]:
            keyword_conditions.append("product_description LIKE %s")
            params.append(f"%{keyword}%")
        
        if keyword_conditions:
            conditions.append(f"({' OR '.join(keyword_conditions)})")
    
    # Combine all conditions
    if conditions:
        base_query += " AND " + " AND ".join(conditions)
    
    base_query += " ORDER BY timestamp DESC"
    
    return base_query, params

def format_search_results(items, search_query, analysis):
    """Format search results for display"""
    response_lines = [
        f"🔍 **Search Results for: '{search_query}'**",
        f"📊 Found {len(items)} matching item(s)",
        "=" * 60
    ]
    
    # Add search context
    if analysis["time_filter"]:
        response_lines.append(f"⏰ Time filter: {analysis['time_filter']}")
    if analysis["product_keywords"]:
        response_lines.append(f"🏷️ Keywords: {', '.join(analysis['product_keywords'])}")
    response_lines.append("")
    
    for i, item in enumerate(items, 1):
        # Calculate time ago
        time_ago = calculate_time_ago(item['timestamp'])
        
        # Format price
        price_str = f"₹{item['price']:.2f}" if item['price'] > 0 else "Price not available"
        
        # Highlight matching keywords in description
        description = highlight_keywords(item['product_description'], analysis["product_keywords"])
        
        # Create item entry
        item_info = [
            f"\n**{i}. {description[:80]}{'...' if len(item['product_description']) > 80 else ''}**",
            f"   💰 Price: {price_str}",
            f"   ⏰ Added: {time_ago}",
            f"   🔗 URL: {item['product_url'][:60]}{'...' if len(item['product_url']) > 60 else ''}",
            f"   📅 Exact Time: {item['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}",
            "-" * 50
        ]
        
        response_lines.extend(item_info)
    
    return {
        "success": True,
        "message": "\n".join(response_lines),
        "items": items,
        "count": len(items),
        "search_analysis": analysis
    }

def format_no_results_response(search_query, analysis):
    """Format response when no results found"""
    suggestions = []
    
    if analysis["product_keywords"]:
        suggestions.append(f"• Try searching for similar products to: {', '.join(analysis['product_keywords'])}")
    
    if analysis["time_range_hours"]:
        suggestions.append(f"• Try expanding your time range beyond {analysis['time_filter']}")
    else:
        suggestions.append("• Try adding a time range like 'yesterday' or 'last week'")
    
    suggestions.append("• Check if the product name matches what you remember")
    suggestions.append("• Try searching with just one keyword")
    
    response = f"""
🔍 **No Results Found for: '{search_query}'**

❌ I couldn't find any cart items matching your search criteria.

💡 **Suggestions:**
{chr(10).join(suggestions)}

🛒 You can also try asking "show me all my cart history" to see everything you've added.
"""
    
    return {
        "success": False,
        "message": response.strip(),
        "items": [],
        "count": 0,
        "search_analysis": analysis
    }

def highlight_keywords(text, keywords):
    """Highlight matching keywords in text (for terminal/text display)"""
    if not keywords:
        return text
    
    highlighted = text
    for keyword in keywords:
        # Simple highlighting with uppercase (since we can't use HTML)
        pattern = re.compile(re.escape(keyword), re.IGNORECASE)
        highlighted = pattern.sub(lambda m: m.group(0).upper(), highlighted)
    
    return highlighted

def calculate_time_ago(timestamp):
    """Calculate human-readable time difference"""
    now = datetime.now()
    diff = now - timestamp
    
    if diff.days > 0:
        if diff.days == 1:
            return "1 day ago"
        else:
            return f"{diff.days} days ago"
    elif diff.seconds > 3600:
        hours = diff.seconds // 3600
        if hours == 1:
            return "1 hour ago"
        else:
            return f"{hours} hours ago"
    elif diff.seconds > 60:
        minutes = diff.seconds // 60
        if minutes == 1:
            return "1 minute ago"
        else:
            return f"{minutes} minutes ago"
    else:
        return "Just now"
