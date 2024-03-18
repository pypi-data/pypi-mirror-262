from genai_agents.tools.base import BaseTool,tool
from pydantic import BaseModel, Field

class GoogleSerperSearchInputSchema(BaseModel):
    search_str: str = Field(description="Query used to search online from Google")

class GoogleSerperSearchOutputSchema(BaseModel):
    response: str = Field(description="Response from the YoutubeSearch tool.")

class GoogleSerperSearchTool(BaseTool):
    name: str = "GoogleSerperSearch Tool"
    description: str = (
        "Tool used to perform a search online using a Google SERP (Search Engine Results Page) scraping API wrapper. "
    )
    @tool(args_schema=GoogleSerperSearchInputSchema, output_schema=GoogleSerperSearchOutputSchema)
    def _run(self, search_str: str = None):
        from genai_agents.tools.tools_db import getSerperScrape
        getSerperScrape(searchString=search_str)