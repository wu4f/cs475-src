import os
import json
import requests
from langchain.agents import AgentExecutor, create_react_agent
from langchain import hub
from langchain.tools import tool
from langchain_google_genai import GoogleGenerativeAI, HarmCategory, HarmBlockThreshold
import readline

# Get VT credentials from environment variable
VIRUSTOTAL_API_KEY = os.getenv("VIRUSTOTAL_API_KEY")
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# Define the LLM
llm = GoogleGenerativeAI(
    model="gemini-1.5-pro-latest",
    temperature=0,
    safety_settings={
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    }
)

@tool
def safebrowsing_url_report(url):
    """(CHANGE ME)"""
    api_url = "https://safebrowsing.googleapis.com/v4/threatMatches:find"
    payload = {
        "client": {
            "clientId": "PSU",
            "clientVersion": "1.0"
        },
        "threatInfo": {
            "threatTypes": ["THREAT_TYPE_UNSPECIFIED", "MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE", "POTENTIALLY_HARMFUL_APPLICATION"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL", "THREAT_ENTRY_TYPE_UNSPECIFIED", "EXECUTABLE"],
            "threatEntries": [
                {"url": url}
            ]
        }
    }
    request_headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(f"{api_url}?key={GOOGLE_API_KEY}", headers=request_headers, data=json.dumps(payload))
    return response.json()

@tool
def virustotal_url_report(url):
    """(CHANGE ME)"""
    api_url = f"https://www.virustotal.com/api/v3/urls"
    request_headers = {"x-apikey": VIRUSTOTAL_API_KEY}
    response = requests.post(api_url, headers=request_headers, data={"url":url})
    if response.status_code == 200:
        response_dict = response.json()
        link = response_dict['data']['links']['self']
        response = requests.get(link, headers=request_headers)
        return response.json()

@tool
def phishtank_url_report(url):
    """(CHANGE ME)"""
    api_url = f"https://checkurl.phishtank.com/checkurl/"
    payload = { 
                 "format" : "json",
                 "url" : url
    }
    request_headers = {"User-Agent": f"phishtank/{os.getenv('USER')}"}
    response = requests.post(api_url, headers=request_headers, data=payload)
    return response.json()['results']['in_database']

# Integrate the tools with the LLM
tools = [virustotal_url_report, safebrowsing_url_report, phishtank_url_report]

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
