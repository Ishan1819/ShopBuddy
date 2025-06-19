from crewai.tools import BaseTool
from backend.bots.amazon_bot import main
from backend.bots.flipkart_bot import search_flipkart
from backend.bots.myntra_bot import search_myntra

def get_search_tool():
    class ProductSearchTool(BaseTool):
        name: str = "ProductSearcher"
        description: str = "Searches products on Amazon, Flipkart, or Myntra using structured filters"

        def _run(self, filters: dict):
            print("🔍 Searching products with filters:", filters)
            platforms = filters.get("platform", [])
            if isinstance(platforms, str):
                platforms = [platforms]
            results = []
            for platform in platforms:
                platform = platform.lower()
                if platform == "amazon":
                    results.extend(main(filters))
                elif platform == "flipkart":
                    results.extend(search_flipkart(filters))
                elif platform == "myntra":
                    results.extend(search_myntra(filters))
                else:
                    results.append({"error": f"Unsupported platform: {platform}"})
            return results

    return ProductSearchTool()
