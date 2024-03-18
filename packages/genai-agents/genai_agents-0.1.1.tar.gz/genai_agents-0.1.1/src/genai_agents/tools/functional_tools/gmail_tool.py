from genai_agents.tools.base import BaseTool, tool
from pydantic import BaseModel, Field


class GmailInputSchema(BaseModel):
    search_str: str = Field(description="Search string to be passed to the input.")


class GmailOutputSchema(BaseModel):
    response: str = Field(description="Response from the agent regarding action performed by gmail.")


class GmailSearchTool(BaseTool):
    name: str = "GmailSearch Tool"
    description: str = (
        "A tool which can be used to perform actions on gmail by using natural language"
    )

    @tool(args_schema=GmailInputSchema, output_schema=GmailOutputSchema)
    def _run(self, search_str: str = None):
        from genai_agents.tools.tools_db import gmail_toolkit

        return gmail_toolkit(searchString=search_str)
