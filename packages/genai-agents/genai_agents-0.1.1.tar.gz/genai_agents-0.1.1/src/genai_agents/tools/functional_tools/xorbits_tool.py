from genai_agents.tools.base import BaseTool, tool
from pydantic import BaseModel, Field


class XorbitsInputSchema(BaseModel):
    search_str: str = Field(description="Search string to be passed to the input.")


class XorbitsOutputSchema(BaseModel):
    response: str = Field(description="Response from the agent regarding action performed by Xorbits.")


class XorbitsSearchTool(BaseTool):
    name: str = "XorbitsSearch Tool"
    description: str = (
        "A tool which can be used to retrieve information from files by performing pandas or numpy code by using natural language."
    )

    @tool(args_schema=XorbitsInputSchema, output_schema=XorbitsOutputSchema)
    def _run(self, search_str: str = None):
        from genai_agents.tools.tools_db import xorbits_toolkit

        return xorbits_toolkit(searchString=search_str)
