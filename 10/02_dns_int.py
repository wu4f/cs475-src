import os
import subprocess
import requests
from langchain.agents import AgentExecutor, create_react_agent
from langchain import hub
from langchain.tools import tool
from langchain_google_genai import GoogleGenerativeAI, HarmCategory, HarmBlockThreshold
import readline

RAPID_API_KEY = os.getenv("RAPID_API_KEY")

# Define the LLM
llm = GoogleGenerativeAI(
    model="gemini-1.5-pro-latest",
    temperature=0,
    safety_settings={
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    }
)

@tool
def cert_domain_search(domain):
    """(CHANGE ME)"""
    url = f"""https://crt.sh/?Identity={domain}&output=json"""
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()

@tool
def email_domain_search(domain):
    """(CHANGE ME)"""
    url = "https://mailcheck.p.rapidapi.com/"
    querystring = {"domain": domain}
    request_headers = {
	"X-RapidAPI-Key": RAPID_API_KEY,
	"X-RapidAPI-Host": "mailcheck.p.rapidapi.com"
    }
    response = requests.get(url, headers=request_headers, params=querystring)
    if response.status_code == 200:
        return response.json()

@tool
def whois_domain_search(domain):
    """(CHANGE ME)"""
    result = subprocess.run(['whois',domain], capture_output=True, text=True, check=True)
    if result:
        return result 

# Integrate the tools with the LLM
tools = [email_domain_search, cert_domain_search, whois_domain_search]

base_prompt = hub.pull("langchain-ai/react-agent-template")
prompt = base_prompt.partial(instructions="Answer the user's request utilizing at most 8 tool calls")

agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

print("Welcome to my application. I am configured with these tools:")
for tool in agent_executor.tools:
    print(f'  Tool: {tool.name} = {tool.description}')

while True:
    line = input("llm>> ")
    try:
        if line:
            result = agent_executor.invoke({"input": line})
            print(result)
        else:
            break
    except Exception as e:
        print(e)
