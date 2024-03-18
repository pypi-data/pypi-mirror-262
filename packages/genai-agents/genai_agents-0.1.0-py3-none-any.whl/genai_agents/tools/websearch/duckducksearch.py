from genai_agents.tools.base import BaseTool, tool
from pydantic import BaseModel, Field


class DuckDuctGoInputSchema(BaseModel):
    search_str: str = Field(description="Search string to be passed to the input.")


class DuckDuctGoOutputSchema(BaseModel):
    response: str = Field(description="Response from the DuckDuckGo search engine.")


class DuckDuckGoSearchTool(BaseTool):
    name: str = "DuckDuckGoSearch Tool"
    description: str = (
        "A tool that can be used to search for words, documents, images, videos, news, maps and text translation using the DuckDuckGo.com search engine. Downloading files and images to a local hard drive."
    )

    @tool(args_schema=DuckDuctGoInputSchema, output_schema=DuckDuctGoOutputSchema)
    def _run(self, search_str: str = None):
        from genai_agents.tools.tools_db import getDuckduckgoSearchResults

        return getDuckduckgoSearchResults(searchString=search_str)