
import os
from langchain_openai import AzureChatOpenAI
from langchain.agents import (
     AgentExecutor,
     AgentType,
     OpenAIFunctionsAgent,
     Tool,
     create_openai_functions_agent,
     initialize_agent,
     load_tools,
     tool,
)
from genai_agents.tools.base import BaseTool,tool
from pydantic import BaseModel, Field
from PIL import Image


#issues - not working
def DallEImageGenerator(inputString):
    llm_2 = AzureChatOpenAI(
    model_name = "gpt4-32k",
    openai_api_version="2023-05-15",
    azure_deployment="gpt4-inference"
    )
    llm=llm_2
    tools = load_tools(["dalle-image-generator"])
    agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=False)
    image = agent.run(inputString)
    return image


