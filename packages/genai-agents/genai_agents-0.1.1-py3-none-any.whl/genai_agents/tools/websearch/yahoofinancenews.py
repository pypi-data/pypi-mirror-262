from genai_agents.tools.base import BaseTool,tool
from pydantic import BaseModel, Field

class YahooFinanceInputSchema(BaseModel):
    search_str: str = Field(description="Query used to search for news on Yahoo Finance")

class YahooFinanceOutputSchema(BaseModel):
    response: str = Field(description="Response from the YahooFinance tool.")

class YahooFinanceTool(BaseTool):
    name: str = "Yahoo Finance News Tool"
    description: str = (
        "A tool designed to explore financial news articles on Yahoo Finance."
    )
    @tool(args_schema=YahooFinanceInputSchema, output_schema=YahooFinanceOutputSchema)
    def _run(self, search_str: str = None):
        from genai_agents.tools.tools_db import yahooFinanceNews

        yahooFinanceNews(searchString=search_str)