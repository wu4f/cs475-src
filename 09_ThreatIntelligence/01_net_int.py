import os
import requests
from langchain.agents import AgentExecutor, create_react_agent
from langchain import hub
from langchain.tools import tool
from langchain_google_genai import GoogleGenerativeAI, HarmCategory, HarmBlockThreshold
import readline

# Get VT credentials from environment variable
VIRUSTOTAL_API_KEY = os.getenv("VIRUSTOTAL_API_KEY")

# Define the LLM
llm = GoogleGenerativeAI(
    model="gemini-1.5-pro-latest",
    temperature=0,
    safety_settings={
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    }
)

@tool
def ip_loc(address):
    """(CHANGE ME) Lookup ipwhois for an IP address. Takes one IP address as a paramater such as 208.91.197.27"""
    url = f"http://ipwho.is/{address}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()

@tool
def ip_report(address):
    """(CHANGE ME) Lookup VirusTotal for an IP address.  Takes one IP address as a paramater such as 208.91.197.27"""
    url = f"https://www.virustotal.com/api/v3/ip_addresses/{address}"
    headers = {"x-apikey": VIRUSTOTAL_API_KEY}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()

# Integrate the tools with the LLM
tools = [ip_loc, ip_report]

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

