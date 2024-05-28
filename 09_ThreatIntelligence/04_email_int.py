import os
import requests
from langchain.agents import AgentExecutor, create_react_agent
from langchain import hub
from langchain_core.pydantic_v1 import BaseModel, Field, root_validator
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
def oop_spam_search(content):
    """Determine if content is spam.  Takes content of e-mail message as a parameter"""
    url = "https://oopspam.p.rapidapi.com/v1/spamdetection"

    payload = {
	"content": "Dear Agent, We are a manufacturing company which specializes in supplying Aluminum Rod with Zinc Alloy Rod to customers worldwide, based in Japan, Asia. We have been unable to follow up payments effectively for transactions with debtor customers in your country due to our distant locations, thus our reason for requesting for your services representation.",
	"allowedLanguages": ["en"]
    }
    headers = {
	"content-type": "application/json",
	"X-RapidAPI-Key": RAPID_API_KEY,
	"X-RapidAPI-Host": "oopspam.p.rapidapi.com"
    }
    response = requests.post(url, json=payload, headers=headers)
    print(response.text)
    if response.status_code == 200:
        return response.json()

@tool
def email_is_spammer(address):
    """Find whether or not an e-mail address has been involved in sending spam.  Takes one e-mail address as a parameter and returns true if it is from a spammer, false otherwise."""
    url = f"http://api.eva.pingutil.com/email?email={address}"
    response = requests.get(url)
    print(response.text)
    if response.status_code == 200:
        return response.json()

@tool
def email_disposable(address):
    """Find whether or not an e-mail address is disposable or temporary.  Takes one e-mail address as a parameter and returns true if it is disposable, false otherwise."""
    url = f"https://open.kickbox.com/v1/disposable/{address}"
    response = requests.get(url)
    print(response.text)
    if response.status_code == 200:
        return response.json()

# Integrate the tools with the LLM
tools = [email_disposable, email_is_spammer, oop_spam_search]

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

