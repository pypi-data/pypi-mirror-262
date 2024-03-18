from genai_agents.tools.base import BaseTool, tool
from pydantic import BaseModel, Field


class DocumentCompareInputSchema(BaseModel):
    search_str: str = Field(description="Search string to be passed to the input.")


class DocumentCompareOutputSchema(BaseModel):
    response: str = Field(description="Response from the agent regarding action performed by DocumentCompare.")


class DocumentCompareSearchTool(BaseTool):
    name: str = "DocumentCompareSearch Tool"
    description: str = (
        "A tool which can be used to by the agent to question uploaded files by the user."
    )

    @tool(args_schema=DocumentCompareInputSchema, output_schema=DocumentCompareOutputSchema)
    def _run(self, search_str: str = None):
        from genai_agents.tools.tools_db import DocuCompare
        
        return DocuCompare(searchString=search_str)