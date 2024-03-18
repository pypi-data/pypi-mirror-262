from genai_agents.tools.base import BaseTool, tool
from pydantic import BaseModel, Field


class NasaInputSchema(BaseModel):
    search_str: str = Field(description="Search string to be passed to the input.")


class NasaOutputSchema(BaseModel):
    response: str = Field(description="Response from the agent regarding action performed by Nasa.")


class NasaSearchTool(BaseTool):
    name: str = "NasaSearch Tool"
    description: str = (
        "A tool which can be used to retrieve information from Nasa's database like images, videos, documents, etc by using natural language."
    )

    @tool(args_schema=NasaInputSchema, output_schema=NasaOutputSchema)
    def _run(self, search_str: str = None):
        from genai_agents.tools.tools_db import nasatool

        return nasatool(searchString=search_str)
