# backend/tools/parser_tool.py

from crewai.tools import BaseTool
from backend.nlp.parser import parse_user_query_with_gemini

class QueryParserTool(BaseTool):
    name: str = "QueryParser"
    description: str = "Parses user shopping query into structured filters."

    def _run(self, input: str) -> dict:

        print("...THIS IS", input)
        op = parse_user_query_with_gemini(input)
        print("Parsed output:", op)
        return parse_user_query_with_gemini(input)

def get_parser_tool():
    print("🔧 Initializing Query Parser Tool...")
    op = QueryParserTool()
    print(op)
    return op


# Give me shoes white in colour from Amazon for men below 7000 rupees and above 4.0 star ratings