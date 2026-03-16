import sys
import json
import os
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools

# Load environment variables
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    print(json.dumps({"error": "OPENROUTER_API_KEY not found in environment"}))
    sys.exit(1)

from pydantic import BaseModel

class FinancialReport(BaseModel):
    ticker: str
    company_name: str
    revenue_brl: str
    net_income_brl: str
    market_cap_brl: str
    key_highlights: str
    sources: str

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No ticker provided"}))
        sys.exit(1)

    ticker = sys.argv[1]

    # Initialize the Agent
    agent = Agent(
        model=OpenAIChat(
            id="meta-llama/llama-3.1-8b-instruct",
            api_key=OPENROUTER_API_KEY,
            base_url="https://openrouter.ai/api/v1",
        ),
        tools=[DuckDuckGoTools()],
        description="You are a Senior Equity Analyst. Research the latest financial data for the given corporate ticker.",
        instructions=[
            f"Research the latest financial data for the ticker: {ticker}.",
            "Focus on the 2024 and 2025 financial results if available.",
            "Retrieve Revenue, Net Income, and Market Cap in BRL.",
            "Also search for P/E Ratio, Debt-to-Equity, and Interest Coverage Ratio.",
            "CRITICAL: EVERY single number, including ratios and percentages, MUST have an explicit source citation (e.g., [SOURCE 1]).",
            "If a metric is missing, explicitly state where you searched (e.g., 'Data not found in sources [Yahoo, Bloomberg]').",
            "Use standard currency formatting (e.g., 'R$ 12.34 Billion').",
            "Maintain strict formatting consistency: no double spaces, clean line breaks.",
            "Market Cap MUST be verified with an 'As of [Date]' clarification and source citation.",
            "Key Highlights MUST include at least 3-4 specific metrics (e.g. EBITDA, ROE) with explicit citations for each.",
        ],
        output_schema=FinancialReport,
        markdown=False,
    )

    prompt = (
        f"Generate a professional, highly consistent financial report for {ticker} in JSON format. "
        "Keys: ticker, company_name, revenue_brl, net_income_brl, market_cap_brl, key_highlights, sources. "
        "Every single metric in the report MUST be followed by an explicit citation in the string. "
        "Format: 'R$ 100 Billion (FY 2024) [SOURCE 1]' or '15.4x [SOURCE 2]'. "
        "The 'key_highlights' MUST contain specific metrics with their respective citations. "
        "Ensure all citations are listed in the 'sources' key with their URLs."
    )

    try:
        response = agent.run(prompt)
        # When output_schema is provided, Agno might return the model instance in content
        # or as the response itself depending on the version.
        # Let's check if it's already a string or a Pydantic model.
        if hasattr(response.content, "model_dump_json"):
            print(response.content.model_dump_json())
        else:
            print(response.content)
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)

if __name__ == "__main__":
    main()
