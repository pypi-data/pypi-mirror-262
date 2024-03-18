from genai_agents.tools.base import BaseTool, tool
from pydantic import BaseModel, Field


class PolygonInputSchema(BaseModel):
    search_str: str = Field(description="Search string to be passed to the input.")


class PolygonOutputSchema(BaseModel):
    response: str = Field(description="Response from the agent regarding action performed by Polygon.")


class PolygonSearchTool(BaseTool):
    name: str = "PolygonSearch Tool"
    description: str = (
        "A tool which can be used to retrieve information regarding current Stock prices and their historical data using natural language."
    )

    @tool(args_schema=PolygonInputSchema, output_schema=PolygonOutputSchema)
    def _run(self, search_str: str = None):
        from genai_agents.tools.tools_db import polygon_toolkit
        return polygon_toolkit(searchString=search_str)