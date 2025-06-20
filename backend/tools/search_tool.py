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
                try:
                    if platform == "amazon":
                        platform_results = main(filters)
                    elif platform == "flipkart":
                        platform_results = search_flipkart(filters)
                    elif platform == "myntra":
                        platform_results = search_myntra(filters)
                    else:
                        platform_results = [{"error": f"Unsupported platform: {platform}"}]

                    if not isinstance(platform_results, list):
                        print(f"❌ Expected a list, but got {type(platform_results)} for {platform}")
                        continue

                    results.extend(platform_results)
                except Exception as e:
                    print(f"❌ Error searching {platform}: {e}")
                    results.append({"error": f"{platform} search failed: {str(e)}"})

            print(f"✅ Total results found: {len(results)}")
            return results

    return ProductSearchTool()
