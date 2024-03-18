
from genai_agents.tools.base import BaseTool, tool
from pydantic import BaseModel, Field


class GoogleFinanceStockInputSchema(BaseModel):
    search_str: str = Field(description="Search string to be passed to the input.")


class GoogleFinanceStockOutputSchema(BaseModel):
    response: str = Field(description="Response from the GoogleFinanceStockSearchtool engine.")


class GoogleFinanceSearchTool(BaseTool):
    name: str = "GoogleFinanceStockSearch Tool"
    description: str = (
        "A tool that uses the Google Finance Tool to get information from the Google Finance page"
    )
    @tool(args_schema=GoogleFinanceStockInputSchema, output_schema=GoogleFinanceStockOutputSchema)
    def _run(self, search_str: str = None):
        from genai_agents.tools.tools_db import googleFinanceStockSearch
        googleFinanceStockSearch(searchString=search_str)  


# #not working
# from langchain.agents import (
#      AgentExecutor,
#      AgentType,
#      OpenAIFunctionsAgent,
#      Tool,
#      create_openai_functions_agent,
#      initialize_agent,
#      load_tools,
#      tool,
# )
# import os
# import pprint

# from langchain_openai import AzureChatOpenAI

# os.environ["SERPAPI_API_KEY"]="09e27394ffb11f7a9d01e7eaf4204191a68c5dc633e4dd17a76b4c739472aead"
# os.environ["SERP_API_KEY"]="09e27394ffb11f7a9d01e7eaf4204191a68c5dc633e4dd17a76b4c739472aead"
# os.environ["AZURE_OPENAI_API_KEY"] = "a20bc67dbd7c47ed8c978bbcfdacf930"
# os.environ["AZURE_OPENAI_ENDPOINT"] = "https://gpt-res.openai.azure.com/"

# llm_1 = AzureChatOpenAI(
# model_name = "gpt4-32k",
# openai_api_version="2023-05-15",
# azure_deployment="gpt4-inference"
# )
# def googleFinanceStockSearch(inputString):
#     llm = llm_1 #OpenAI(temperature=0)
    
#     tools = load_tools(["google-scholar", "google-finance"], llm=llm)
#     agent = initialize_agent(
#     tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=False
#     )
#     results= agent.run(inputString)
#     finalResult= pprint.pp(results)
#     print(finalResult)
#     return results

# print(googleFinanceStockSearch("What is google's current stock"))
