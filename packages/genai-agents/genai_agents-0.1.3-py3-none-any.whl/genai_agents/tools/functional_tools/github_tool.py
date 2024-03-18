from genai_agents.tools.base import BaseTool, tool
from pydantic import BaseModel, Field


class GithubInputSchema(BaseModel):
    search_str: str = Field(description="Search string to be passed to the input.")


class GithubOutputSchema(BaseModel):
    response: str = Field(description="Response from the agent regarding action performed by Github.")


class GithubSearchTool(BaseTool):
    name: str = "GithubSearch Tool"
    description: str = (
        "A tool which can be used to retrieve information regarding respective repository like code changes, commits, active PRs, issues, etc by using natural language."
    )

    @tool(args_schema=GithubInputSchema, output_schema=GithubOutputSchema)
    def _run(self, search_str: str = None):
        from genai_agents.tools.tools_db import github_toolkit

        return github_toolkit(searchString=search_str)
