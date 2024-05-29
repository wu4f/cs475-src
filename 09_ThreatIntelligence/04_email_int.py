import os
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
def oop_spam_search(content):
    """(CHANGE ME) Determine if content is spam.  Takes content of an email as a parameter and returns ..."""
    url = "https://oopspam.p.rapidapi.com/v1/spamdetection"

    payload = {
	"content": content,
	"allowedLanguages": ["en"]
    }
    headers = {
	"content-type": "application/json",
	"X-RapidAPI-Key": RAPID_API_KEY,
	"X-RapidAPI-Host": "oopspam.p.rapidapi.com"
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()

@tool
def email_is_spammer(address):
    """(CHANGE ME) Determine if e-mail address is a spammer's.  Takes an e-mail address as a parameter and returns ..."""
    url = f"http://api.eva.pingutil.com/email?email={address}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()

# Integrate the tools with the LLM
tools = [email_is_spammer, oop_spam_search]

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

