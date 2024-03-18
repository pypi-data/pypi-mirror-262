from genai_agents.tools.base import BaseTool



class GoogleSerperSearchTool(BaseTool):
    name = "Google Serper Search"
    def _run(self, search_str: str = None):
        from genai_agents.tools.tools_db import getSerperScrape
        getSerperScrape(searchString=search_str)
