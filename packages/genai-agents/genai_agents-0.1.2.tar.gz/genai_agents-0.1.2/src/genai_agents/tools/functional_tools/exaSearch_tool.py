from genai_agents.tools.base import BaseTool, tool
from pydantic import BaseModel, Field


class exaSearchInputSchema(BaseModel):
    search_str: str = Field(description="Search string to be passed to the input.")


class exaSearchOutputSchema(BaseModel):
    response: str = Field(description="Response from the agent regarding action performed by exaSearch.")


class exaSearchTool(BaseTool):
    name: str = "exaSearchSearch Tool"
    description: str = (
        "A tool which can be used to do a Exa Search."
    )

    @tool(args_schema=exaSearchInputSchema, output_schema=exaSearchOutputSchema)
    def _run(self, search_str: str = None):
        from genai_agents.tools.tools_db import exaSearch

        return exaSearch(searchString=search_str)
