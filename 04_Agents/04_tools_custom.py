from langchain_community.tools import DuckDuckGoSearchResults
from langchain.tools import Tool
from langchain.prompts import PromptTemplate
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain_google_genai import GoogleGenerativeAI
from langchain.chains import LLMChain
import readline
import requests
from bs4 import BeautifulSoup

llm = GoogleGenerativeAI(model="gemini-pro")

def fetch_web_page(url):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content,"html.parser")
    return soup.get_text()

web_fetch_tool = Tool.from_function(
  func = fetch_web_page,
  name = "WebFetcher",
  description="Fetches the content of a web page"
)

def lookup_site(address):
    resp = requests.get(f"https://http-observatory.security.mozilla.org/api/v1/getHostHistory?host={address}")
    print(resp.text)
    return resp.text

site_tool = Tool.from_function(
    func = lookup_site,
    name = "WebSite information",
    description = "Given a web site address, it will return security information about it including a graded evaluation of its security configuration"
)

def lookup_phishing(address):
    resp = requests.get(f"https://phishstats.info:2096/api/phishing?_where=(ip,eq,{address})")
    urls = []
    for entry in resp.json():
        urls.append(entry['url'])
    return urls

phish_tool = Tool.from_function(
    func = lookup_phishing,
    name = "PhishStatsFetcher",
    description = "Returns a list of phishing URLs that have been sent by a given IP address"
)

summary_prompt_template = "Summarize the following content: {content}"
llm_chain = LLMChain(
    llm=llm,
    prompt=PromptTemplate.from_template(summary_prompt_template)
)

summary_tool = Tool.from_function(
    func=llm_chain.run,
    name="Summarizing tool",
    description="Summarizes a web page given its URL"
)

ddg_search = DuckDuckGoSearchResults()

tools = [ddg_search, web_fetch_tool, summary_tool, phish_tool, site_tool]

prompt = hub.pull("hwchase17/react")

agent = create_react_agent(llm,tools,prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

print("Welcome to my application.  I can search the web, fetch web pages, summarize content, determine whether or not an IP address has sent phishing lures, and analyze web servers.")
while True:
    try:
        line = input("llm>> ")
        if line:
            result = agent_executor.invoke({"input":line})
            print(result)
        else:
            break
    except:
        break

#print(agent_executor.invoke({"input":"Search for foo"}))
#print(agent_executor.invoke({"input":"Find a site that describes Python requests and summarize what it does."}))
