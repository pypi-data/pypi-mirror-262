from genai_agents.tools.base import BaseTool,tool
from pydantic import BaseModel, Field

class WikipediaToolInputSchema(BaseModel):
    search_str: str = Field(description="Query used to search the Wikipedia API")

class WikipediaToolOutputSchema(BaseModel):
    response: str = Field(description="Response from the Wikipedia tool.")

class WikipediaTool(BaseTool):
    name: str = "Wikipedia Tool"
    description: str = (
        "A tool designed to Tool that searches the Wikipedia API for a specific query."
    )
    @tool(args_schema=WikipediaToolInputSchema, output_schema=WikipediaToolOutputSchema)
    def _run(self, search_str: str = None):
        from genai_agents.tools.tools_db import wikipediaTool

        wikipediaTool(searchString=search_str)