from genai_agents.tools.base import BaseTool, tool
from pydantic import BaseModel, Field


class SerperSpecificInputSchema(BaseModel):
    search_str: str = Field(description="Search string to be passed to the input.")


class SerperSpecificOutputSchema(BaseModel):
    response: str = Field(description="Response from the agent regarding action performed by SerperSpecific.")


class SerperSpecificSearchTool(BaseTool):
    name: str = "SerperSpecificSearch Tool"
    description: str = (
        "A tool which can be used to scrape information from the search engine for a specific type and period using natural language"
    )

    @tool(args_schema=SerperSpecificInputSchema, output_schema=SerperSpecificOutputSchema)
    def _run(self, search_str: str = None):
        from genai_agents.tools.tools_db import getSerperScrapeForSpecificTypeAndPeriod

        return getSerperScrapeForSpecificTypeAndPeriod(searchString=search_str)
