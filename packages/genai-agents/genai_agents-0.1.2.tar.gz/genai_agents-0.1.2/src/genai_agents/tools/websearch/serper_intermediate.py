from genai_agents.tools.base import BaseTool, tool
from pydantic import BaseModel, Field


class SerperIntermediateInputSchema(BaseModel):
    search_str: str = Field(description="Search string to be passed to the input.")


class SerperIntermediateOutputSchema(BaseModel):
    response: str = Field(description="Response from the agent regarding action performed by SerperIntermediate.")


class SerperIntermediateSearchTool(BaseTool):
    name: str = "SerperIntermediateSearch Tool"
    description: str = (
        "A tool which can be useful for when you need to ask with search."
    )

    @tool(args_schema=SerperIntermediateInputSchema, output_schema=SerperIntermediateOutputSchema)
    def _run(self, search_str: str = None):
        from genai_agents.tools.tools_db import googleSerperSearchIntermediateQuestions

        return googleSerperSearchIntermediateQuestions(searchString=search_str)