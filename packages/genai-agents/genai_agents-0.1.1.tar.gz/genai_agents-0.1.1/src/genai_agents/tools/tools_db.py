import asyncio
import os
import pprint
import dotenv
import xorbits.pandas as pd
from exa_py import Exa
from genai_agents.utils.yamlParse import getYamlAttribute
from langchain import hub
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
import logging
#from langchain.llms import CTransformers
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import LLMChain, RetrievalQA
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.agent_toolkits import (
     AzureCognitiveServicesToolkit,
     GmailToolkit,
     O365Toolkit,
     PlayWrightBrowserToolkit,
     PowerBIToolkit,
     create_pbi_agent,
     create_sql_agent,
)
from langchain_community.agent_toolkits.github.toolkit import GitHubToolkit
from langchain_community.agent_toolkits.nasa.toolkit import NasaToolkit
from langchain_community.agent_toolkits.polygon.toolkit import PolygonToolkit
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings, OpenAI, OpenAIEmbeddings
from langchain_community.llms import CTransformers
from langchain_community.tools import (
     DuckDuckGoSearchRun,
     ElevenLabsText2SpeechTool,
     WikipediaQueryRun,
     YouTubeSearchTool,
)
from langchain_community.tools.google_jobs import GoogleJobsQueryRun
from langchain_community.tools.playwright.utils import create_async_playwright_browser
from langchain_community.tools.yahoo_finance_news import YahooFinanceNewsTool
from langchain_community.utilities import GoogleSerperAPIWrapper, WikipediaAPIWrapper
from langchain_community.utilities.github import GitHubAPIWrapper
from langchain_community.utilities.google_jobs import GoogleJobsAPIWrapper
from langchain_community.utilities.nasa import NasaAPIWrapper
from langchain_community.utilities.polygon import PolygonAPIWrapper
from langchain_community.utilities.powerbi import PowerBIDataset
from langchain_community.utilities.sql_database import SQLDatabase
from genai_agents.tools.functional_tools import *
from langchain_core.messages import SystemMessage
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_exa import ExaSearchRetriever, TextContentsOptions
from genai_agents.tools.functional_tools import *
from langchain_experimental.agents.agent_toolkits import create_xorbits_agent
from genai_agents.tools.websearch import *
from genai_agents.utils.extraction import extract_cls_method_params
import os


dotenv.load_dotenv()

TOOLS_DICT = [
    {
        "category": "Search",
        **DuckDuckGoSearchTool.get_tool_info(),
        "output": "Search results after using the tool",
    },
    {
        "category": "gmail",
        **GmailSearchTool.get_tool_info(),
        "output": "Gmail results after using the tool.", 
    },
    {
        "category" : "Search",
        **GithubSearchTool.get_tool_info(),
        "output": "Github results after using the tool.",
    },
    {
        "category" : "Search",
        **YoutubeSearchTool.get_tool_info(),
        "output": "Youtube results after using the tool.",
    },
    {
        "category" : "Compare",
        **DocumentCompareSearchTool.get_tool_info(),
        "output": "Document comparison results after using the tool.",
    },
    {
        "category" : "Search",
        **NasaSearchTool.get_tool_info(),
        "output": "Nasa results after using the tool.",
    },
    {
        "category" : "Search",
        **OpenWeatherMapSearchTool.get_tool_info(),
        "output": "OpenWeatherMap results after using the tool.",
    },
    {
        "category" : "Search",
        **PolygonSearchTool.get_tool_info(),
        "output": "Polygon results after using the tool.",
    },
    {
        "category" : "Search",
        **SqlSearchTool.get_tool_info(),
        "output": "Sql results after using the tool.",
    },
    {
        "category" : "Search",
        **XorbitsSearchTool.get_tool_info(),
        "output": "Xorbits results after using the tool.",
    },
    {
        "category" : "Search",
        **GoogleSerperSearchTool.get_tool_info(),
        "output": "GoogleSerper results after using the tool.",
    },
    {
        "category" : "Search",
        **YoutubeSearchTool.get_tool_info(),
        "output": "Youtube results after using the tool.",
    },
    {
        "category" : "Search",
        **GoogleFinanceSearchTool.get_tool_info(),
        "output": "GoogleFinance results after using the tool.",
    },
    {
        "category" : "Search",
        **WikipediaTool.get_tool_info(),
        "output": "Wikipedia results after using the tool.",
    },
    {
        "category" : "Search",
        **YahooFinanceTool.get_tool_info(),
        "output": "YahooFinance results after using the tool.",
    },
    {
        "category" : "Search",
        **SerperSpecificSearchTool.get_tool_info(),
        "output": "SerperSpecific results after using the tool.",
    },
    {
        "category" : "Search",
        **SerperIntermediateSearchTool.get_tool_info(),
        "output": "SerperIntermediate results after using the tool.",
    },
    {
        "category" : "Search",
        **exaSearchTool.get_tool_info(),
        "output": "ExaSearch results after using the tool.",
    },
]
TOOLS_DICT_MAPPING = {tool["tool_name"]: tool for tool in TOOLS_DICT} # This is created for faster lookups when using tools in the agents
BASE_URL= getYamlAttribute('BASE_URL')
DEPLOYMENT_NAME= getYamlAttribute('DEPLOYMENT_NAME')
MODEL_NAME= getYamlAttribute('MODEL_NAME')
OPENAI_API_VERSION= getYamlAttribute('OPENAI_API_VERSION')
API_KEY = os.environ.get('AZURE_OPENAI_API_KEY')
llm_1 = AzureChatOpenAI(azure_deployment=DEPLOYMENT_NAME,
model_name = MODEL_NAME,
openai_api_version=OPENAI_API_VERSION,
openai_api_key=API_KEY,
azure_endpoint=BASE_URL)
serper_api_key = os.environ.get('SERPER_API_KEY')
os.environ["SERPER_API_KEY"] = serper_api_key

#verified
def getDuckduckgoSearchResults(searchString):
     logging.debug(searchString)
     search_tool = DuckDuckGoSearchRun()
     result=search_tool.run(searchString)
     logging.debug(f'duckduck output:{result}')
     return result


def getYoutubeSearchResults(searchString):
    tool = YouTubeSearchTool()
    result = tool.run(searchString)
    return result
    

def getSerperScrapeForSpecificTypeAndPeriod(searchString, type='news', tbs='qdr:y'):
    search = GoogleSerperAPIWrapper(type=type, tbs=tbs)
    logging.debug(f"searchString: {searchString}, type: {type}, tbs: {tbs}")
    output=search.results(searchString)
    pprint.pp(output)
    return output

def googleSerperSearchIntermediateQuestions(searchString):
    llm = llm_1 
    search = GoogleSerperAPIWrapper()
    tools = [
        Tool(
            name="Intermediate Answer",
            func=search.run,
            description="useful for when you need to ask with search",
        )
    ]
    self_ask_with_search = initialize_agent(
        tools, llm, agent=AgentType.SELF_ASK_WITH_SEARCH, verbose=False
    )
    results=self_ask_with_search.run(searchString)
    finalResult = pprint.pp(results)
    logging.debug(finalResult)
    return results

def googleFinanceStockSearch(searchString):
    os.environ["SERPAPI_API_KEY"]= os.environ.get('SERPER_API_KEY')
    os.environ["SERP_API_KEY"]= os.environ.get('SERPER_API_KEY')
    os.environ["AZURE_OPENAI_API_KEY"] = os.environ.get('AZURE_OPENAI_API_KEY')
    os.environ["AZURE_OPENAI_ENDPOINT"] = getYamlAttribute('BASE_URL')
    llm_2 = AzureChatOpenAI(
    model_name = MODEL_NAME,
    openai_api_version= getYamlAttribute('OPENAI_API_VERSION'),
    azure_deployment= getYamlAttribute('DEPLOYMENT_NAME'),
    )
    llm = llm_2 
    tools = load_tools(["google-scholar", "google-finance"], llm=llm)
    agent = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=False
    )
    results= agent.run(searchString)
    finalResult= pprint.pp(results)
    logging.debug(finalResult)
    return results





def googleJobsSearch(input):
        os.environ["SERP_API_KEY"] = os.environ.get('SERP_API_KEY')
        tool = GoogleJobsQueryRun(api_wrapper=GoogleJobsAPIWrapper())
        results= tool.run(input)
        pprint.pp(results)
        logging.debug(results)
        return results

def yahooFinanceNews(searchString):
    llm = llm_1 
    tools = [YahooFinanceNewsTool()]
    tool = initialize_agent(
        tools,
        llm,
        handle_parsing_errors=True,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=False,
    )
    results= tool.run(searchString)
    pprint.pp(results)
    logging.debug(results)
    return results


def wikipediaTool(searchString):
    api_wrapper = WikipediaAPIWrapper(top_k_results=2, doc_content_chars_max=10000)
    tool = WikipediaQueryRun(api_wrapper=api_wrapper)
    results= tool.run(searchString)
    pprint.pp(results)
    logging.debug(results)
    return results
  
 
# def O365(searchString):
#     toolkit = O365Toolkit()
#     tools = toolkit.get_tools()
#     llm = llm_1
#     agent = initialize_agent(
#     tools=toolkit.get_tools(),
#     llm=llm,
#     verbose=False,
#     agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
#     )
#     result = agent.invoke(searchString)
#     return result

def gmail_toolkit(searchString):
    credentials = getYamlAttribute('GMAIL_CREDS')
    toolkit = GmailToolkit()
    tools = toolkit.get_tools()
    base_prompt = hub.pull("langchain-ai/openai-functions-template")
    instructions = "Use the Gmail API to search for emails in your inbox and return the results."
    prompt = base_prompt.partial(instructions=instructions)
    llm = llm_1
    agent = create_openai_functions_agent(llm, toolkit.get_tools(), prompt)
    agent_executor = AgentExecutor(
    agent=agent,
    tools=toolkit.get_tools(),
    verbose=True,
    )
    result = agent_executor.invoke({"input" : searchString})
    return result

def open_weather_app(searchString):
    llm = llm_1
    os.environ["OPENWEATHERMAP_API_KEY"] = os.environ.get('OPENWEATHERMAP_API_KEY')
    tools = load_tools(["openweathermap-api"], llm)
    agent_chain = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    )
    result = agent_chain.invoke(searchString)
    logging.debug(result)
    return result

def nasatool(searchString):
    llm = llm_1
    nasa = NasaAPIWrapper()
    toolkit = NasaToolkit.from_nasa_api_wrapper(nasa)
    agent = initialize_agent(
        toolkit.get_tools(), llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
    )
    result = agent.invoke(searchString)   
    logging.debug(result)
    return result

def github_toolkit(searchString):
    os.environ["GITHUB_APP_ID"] = os.environ.get('GITHUB_APP_ID')
    os.environ["GITHUB_APP_PRIVATE_KEY"] = getYamlAttribute('GITHUB_APP_PRIVATE_KEY')
    os.environ["GITHUB_REPOSITORY"] = getYamlAttribute('GITHUB_REPOSITORY') 
    llm = llm_1
    github = GitHubAPIWrapper()
    toolkit = GitHubToolkit.from_github_api_wrapper(github)
    tools = toolkit.get_tools()
    agent = initialize_agent(
        tools=tools, llm=llm, agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION, verbose=True
    )
    result = agent.run(searchString)
    logging.debug(result)
    return result

# def powerbi(searchString):
#     llm = llm_1
#     toolkit = PowerBIToolkit(
#     powerbi=PowerBIDataset(
#         dataset_id="ca5fd8b4-6ce5-4d29-bca6-3871473c5013",
#         table_names=["Table"],
#         credential=DefaultAzureCredential(),
#     ),
#     llm=llm,
#     )
#     agent_executor = create_pbi_agent(
#     llm=llm,
#     toolkit=toolkit,
#     verbose=True,
#     )
#     result = agent_executor.run(searchString)
#     return result

def xorbits_toolkit(searchString):
    xorbotsCSVFileName = getYamlAttribute('xorbotsCSVFileName')
    data = pd.read_csv(xorbotsCSVFileName)
    llm = llm_1
    agent = create_xorbits_agent(llm, data, verbose=True, handle_parsing_errors=True)
    result = agent.run(searchString)
    logging.debug(result)
    return result

def sql_toolkit(searchString):
    sqlLiteDBName = getYamlAttribute('sqlLiteDBName')
    db = SQLDatabase.from_uri(sqlLiteDBName)
    llm = llm_1
    agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=True)
    result = agent_executor.invoke(searchString)
    logging.debug(result)
    return result

def polygon_toolkit(searchString):
    os.environ["POLYGON_API_KEY"] = os.environ.get('POLYGON_API_KEY')
    llm = llm_1
    instructions = """You are an assistant."""
    base_prompt = hub.pull("langchain-ai/openai-functions-template")
    prompt = base_prompt.partial(instructions=instructions)
    polygon = PolygonAPIWrapper()
    toolkit = PolygonToolkit.from_polygon_api_wrapper(polygon)
    agent = create_openai_functions_agent(llm, toolkit.get_tools(), prompt)
    agent_executor = AgentExecutor(
    agent=agent,
    tools=toolkit.get_tools(),
    verbose=True,
    )
    result = agent_executor.invoke({"input" : searchString})
    logging.debug(result)
    return result

def DocuCompare(searchString):
    os.environ["AZURE_OPENAI_ENDPOINT"] = getYamlAttribute('BASE_URL')
    deployment_name = getYamlAttribute('EMBEDDING_DEPLOYMENT')
    llm = llm_1
    tools = []
    directory = getYamlAttribute('pdfFile')  # Specify the directory path here
    files = []
    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):
            file_path = os.path.join(directory, filename)
            file_info = {"name": os.path.splitext(filename)[0], "path": file_path}
            files.append(file_info)
    for file in files:
        loader = PyPDFLoader(file["path"])
        pages = loader.load_and_split()
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        docs = text_splitter.split_documents(pages)
        embeddings = AzureOpenAIEmbeddings(
            azure_deployment=deployment_name,
            openai_api_version=getYamlAttribute('OPENAI_API_VERSION'),
        )
        retriever = FAISS.from_documents(docs, embeddings).as_retriever()
        tools.append(
            Tool(
                name=file["name"],
                description=f"useful when you want to answer questions about {file['name']}",
                func=RetrievalQA.from_chain_type(llm=llm, retriever=retriever),
            )
        )
    agent = initialize_agent(
    agent=AgentType.OPENAI_FUNCTIONS,
    tools=tools,
    llm=llm,
    verbose=True,
    )
    result = agent({"input": searchString})
    logging.debug(result)
    return result

# def azure_cogs_toolkit(searchString):
#     os.environ["AZURE_COGS_KEY"] = os.environ.get('AZURE_COGS_KEY')
#     os.environ["AZURE_COGS_ENDPOINT"] = os.environ.get('AZURE_COGS_ENDPOINT')
#     os.environ["AZURE_COGS_REGION"] = os.environ.get('AZURE_COGS_REGION')
#     llm = llm_1
#     toolkit = AzureCognitiveServicesToolkit()
#     agent = initialize_agent(
#     tools=toolkit.get_tools(),
#     llm=llm,
#     agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
#     verbose=True,
#     )
#     result = agent.run(searchString)
#     return result

#utility function
def ExaAdvToolSetup22():
    
   # exa = Exa(api_key=os.environ["Exa_API_KEY"])
    exa = Exa(api_key=os.environ["EXA_API_KEY"])


    @tool
    def search(query: str, include_domains=None, start_published_date=None):
        """Search for a webpage based on the query.
        Set the optional include_domains (list[str]) parameter to restrict the search to a list of domains.
        Set the optional start_published_date (str) parameter to restrict the search to documents published after the date (YYYY-MM-DD).
        """
        return exa.search_and_contents(
            f"{query}",
            use_autoprompt=True,
            num_results=getYamlAttribute('EXA_NUM_SEARCH_RESULTS'), #2
            include_domains=include_domains,
            start_published_date=start_published_date,
        )

#utility function
def ExaAdvToolSetup():
    
   # exa = Exa(api_key=os.environ["Exa_API_KEY"])
    exa = Exa(api_key=os.environ["EXA_API_KEY"])


    @tool
    def search(query: str, include_domains=None, start_published_date=None):
        """Search for a webpage based on the query.
        Set the optional include_domains (list[str]) parameter to restrict the search to a list of domains.
        Set the optional start_published_date (str) parameter to restrict the search to documents published after the date (YYYY-MM-DD).
        """
        return exa.search_and_contents(
            f"{query}",
            use_autoprompt=True,
            num_results= getYamlAttribute('EXA_NUM_SEARCH_RESULTS'),
            include_domains=include_domains,
            start_published_date=start_published_date,
        )
    @tool
    def find_similar(url: str):
        """Search for webpages similar to a given URL.
        The url passed in should be a URL returned from `search`.
        """
        return exa.find_similar_and_contents(url, num_results=5)

    @tool
    def get_contents(ids: list[str]):
        """Get the contents of a webpage.
        The ids passed in should be a list of ids returned from `search`.
        """
        return exa.get_contents(ids)


    tools = [search, get_contents, find_similar]
    return tools
    
#utility function  
def ExaToolSetup():
    
    exa = Exa(api_key=os.environ["EXA_API_KEY"])


    @tool
    def search(query: str):
        """Search for a webpage based on the query."""
        return exa.search(f"{query}", use_autoprompt=True, num_results=5)


    @tool
    def find_similar(url: str):
        """Search for webpages similar to a given URL.
        The url passed in should be a URL returned from `search`.
        """
        return exa.find_similar(url, num_results=5)


    @tool
    def get_contents(ids: list[str]):
        """Get the contents of a webpage.
        The ids passed in should be a list of ids returned from `search`.
        """
        return exa.get_contents(ids)


    tools = [search, get_contents, find_similar]
    return tools
#working for small size results - can give issues when context length is higher than the maximm supported
def exaSearch(searchString):
    llm = llm_1
    tools = ExaAdvToolSetup()
    system_message = SystemMessage(
        content="You are a web researcher who answers user questions within the context length by looking up information on the internet and retrieving contents of helpful documents. Cite your sources."
    )

    agent_prompt = OpenAIFunctionsAgent.create_prompt(system_message)
    agent = OpenAIFunctionsAgent(llm=llm, tools=tools, prompt=agent_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    results= agent_executor.run(searchString)
    logging.debug(results)
    return results

def DallEImageGenerator(searchString):
    llm=llm_1
    tools = load_tools(["dalle-image-generator"])
    agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=False)
    image = agent.run(searchString)
    return image
        
#not working - to be implemented later
def text2Speech(searchString):
    llm = llm_1
    tools = load_tools(["eleven_labs_text2speech"])
    agent = initialize_agent(
      tools=tools,
      llm=llm,
      agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
      verbose=True,
    )
    audio_file = agent.run(searchString)
    tts = ElevenLabsText2SpeechTool()
    tts.stream_speech("this is bhaskar")
    #tts.play(audio_file)
    return audio_file

def test1():
      pat="What is the hometown of the reigning men's U.S. Open champion?"
      pat1="Collect and summarize recent news articles, press releases, and market analyses related to the stock  NOKIA and its industry"

      result= googleSerperSearchIntermediateQuestions(pat)
    
      result= getSerperScrapeForSpecificTypeAndPeriod("Tesla inc ", type="news", tbs="qdr:m")
      print(f"the result is: {result}")

      result = getSerperScrapeForSpecificTypeAndPeriod("Get best tourist places in India ", type="images", tbs="qdr:y")
            
      print(f"the result is: {result}")
      
      
def test2():
    # googleSerperSearch(pat1)
    # googleSerperSearch("Tesla inc ", type="news", tbs="qdr:m")
    # getSerperScrape("Tesla inc ", type="news", tbs="qdr:m")
    # O365("Could you search in my inbox and let me know if there's any mail?")        
    # gmail_toolkit("Create a new email with content on congraluations on your promotion to tanish@aiplanet.com and send it.")
    # open_weather_app("What is the weather in New York?")
    # nasatool("What is the latest news from NASA?")
    # print(github_toolkit("List all the code files and the content of files."))
    # powerbi("Describe Table")
    # xorbits_toolkit("What is the dataset about?")
    sql_toolkit("List the total sales per artist. Which artist's fans spent the most?")
    # polygon_toolkit("What is the last day's stock price of apple?")
    # playwright_toolkit("What are the headers on langchain.com?")   # requires async-await
    # DocuCompare("What is the difference between the two documents?")  
 


# Example Usage:
if __name__ == "__main__":


    role='Private Investment Advisor'
    goal="""Impress your customers with full analyses over stocks
        and completer investment recommendations"""
    backstory="""You're the most experienced investment advisor
        and you combine various analytical insights to formulate
        strategic investment advice. You are now working for
        a super important customer you need to impress."""
    task= """
            Collect and summarize recent news articles, press
            releases, and market analyses related to the stock and
            its industry.
            Pay special attention to any significant events, market
            sentiments, and analysts' opinions. Also include upcoming 
            events like earnings and others.
    
            Your final answer MUST be a report that includes a
            comprehensive summary of the latest news, any notable
            shifts in market sentiment, and potential impacts on 
            the stock.
            Also make sure to return the stock ticker.
            Make sure to use the most recent data as possible.
            Selected company by the customer:Nokia"""
            
    
    
 
          
    #wikipediaTool()
    Input= role + goal + backstory + task
    jobs= "give me an entry level job posting related to physics"
    #openAISearchJobs(jobs)
    #results= googleJobsSearch(jobs)
    # result= googleFinanceStockSearch("please get stock price of Nokia")
    #print(f"the result is: {results}")
    #tool = GoogleJobsQueryRun(api_wrapper=GoogleJobsAPIWrapper())

    #results=tool.run("Can I get an entry level job posting related to physics")
    #rl=pprint.pp(results)
    #jj="give me an entry level job posting related to physics"
   # googleJobsSearch(jj)
    #print(kk)
    #googleFinance("what is Nokia stock")
    
    pat2=" Can you please summarise only sachin tendulkar  world records"
    pat3= "How does Microsoft feels today comparing with Nvidia?"
    pat4="What happens to Nokia stocks today "
    pat5 = "Tell me a joke and read it out for me."
    results=wikipediaTool(pat2)
    print(f"the result wikipedia is: {results}")
    results = yahooFinanceNews(pat4)
    print(f"the result yahooFinanceNews is: {results}")

    results= getSerperScrapeForSpecificTypeAndPeriod(searchString="Nokia", type="news",tbs="qdr:m" )
    print(f"the result getSerperScrapeForSpecificTypeAndPeriod is: {results}")

    
    pat6="Summarize for me a fascinating article about cats."
    pat7= "Summarize for me an interesting article about AI from lesswrong.com published in  2024 not exeeding 2000 words."
    pat8="search for latest trends in Covid-19 and Cancer treatment that includes medicines, physical exercises, overall management and prevention aspects"
    # audio_file= text2Speech(pat5)
    pat9="Create an image of a halloween night at a haunted museum"
    results=getDuckduckgoSearchResults(pat8)
    #results= exaSearch(pat8)
    
    # image= DallEImageGenerator(pat9)
    print(f"the result is: {results}")
    # test1()
    # test2()
#Tool_description= ["getSerperScrape", "getSerperScrape:description"]
