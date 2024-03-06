# Import things that are needed generically
#from langchain.agents import Tool
from langchain_community.tools import DuckDuckGoSearchResults
from langchain.tools import Tool
from langchain.prompts import PromptTemplate
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAI
from langchain.chains import LLMChain
import requests
from bs4 import BeautifulSoup

def fetch_web_page(url: str) -> str:
    """Get the message of the day"""
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content,"html.parser")
    return soup.get_text()

ddg_search = DuckDuckGoSearchResults()

web_fetch_tool = Tool.from_function(
  fetch_web_page,
  name="WebFetcher",
  description="Fetches the content of a web page"
)

llm = GoogleGenerativeAI(model="gemini-pro")
prompt_template = "Summarize the following content: {content}"
llm_chain = LLMChain(
    llm=llm,
    prompt=PromptTemplate.from_template(prompt_template)
)

summarize_tool = Tool.from_function(
    func=llm_chain.run,
    name="Summarizer",
    description="Summarizes a web page"
)
tools = [ddg_search, web_fetch_tool, summarize_tool]
#tools = [
#    Tool(
#        name="motd",
#        func=get_motd,
#        description="Useful when you need to get the message of the day",
#    ),
#]

prompt = hub.pull("hwchase17/react")

agent = create_react_agent(llm,tools,prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

#print(agent_executor.invoke({"input":"Search for foo"}))
print(agent_executor.invoke({"input":"Find a site that describes Python requests and summarize what it does."}))
