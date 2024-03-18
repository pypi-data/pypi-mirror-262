from genai_agents.tools.base import BaseTool, tool
from pydantic import BaseModel, Field


class GoogleJobsInputSchema(BaseModel):
    search_str: str = Field(description="Search string to be passed to the input.")


class GoogleJobsOutputSchema(BaseModel):
    response: str = Field(description="Response from the GoogleJobsQuery engine.")


class GoogleJobSearchTool(BaseTool):
    name: str = "GoogleJobsSearch Tool"
    description: str = (
        "A tool that can be used to access the GoogleJobs API and search for jobs online "
    )
    @tool(args_schema=GoogleJobsInputSchema, output_schema=GoogleJobsOutputSchema)
    def _run(self, search_str: str = None):
        from genai_agents.tools.tools_db import googleJobsSearch
        googleJobsSearch(searchString=search_str)
