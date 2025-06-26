import readline
from langchain import hub
from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain.tools import tool
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_google_genai import GoogleGenerativeAI
import os
import subprocess

from langsmith import Client
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = f"LangSmith Introduction"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
client = Client()

chat_history = InMemoryChatMessageHistory()
def get_history():
    return chat_history

# LLM
llm = GoogleGenerativeAI(model="gemini-2.0-flash")

@tool("list_running_services", return_direct=False)
def list_running_services():
    """Retrieves the list of running services on the host"""
    result = subprocess.run(['systemctl', 'list-units', '--type=service', '--state=running'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result

@tool("list_installed_packages", return_direct=False)
def list_installed_packages():
    # Run the dpkg-query command to get the list of installed packages
    """Retrieves the list of installed packages and their versions on the host"""
    result = subprocess.run(['dpkg-query', '-W', '-f=${Package} ${Version}\n'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result

@tool("list_package_vulnerabilities", return_direct=False)
def is_package_vulnerable(package_name):
    """Look up vulnerabilities of a package across all versions given the name of the package given as a string.  Find authors of package updates."""
    result = subprocess.run(['apt', 'changelog', package_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return(result)

tools = [list_running_services, list_installed_packages,is_package_vulnerable]

base_prompt = hub.pull("hwchase17/structured-chat-agent")
prompt = base_prompt.partial(instructions="Answer the user's request utilizing at most 8 tool calls")

agent = create_structured_chat_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)
agent_with_memory = RunnableWithMessageHistory(
    agent_executor,
    get_history,
    input_messages_key="input",
    history_messages_key="chat_history",
)

print("Welcome to my application. I am configured with these tools:")
for tool in agent_executor.tools:
  print(f'  Tool: {tool.name} = {tool.description}')

while True:
    line = input("llm>> ")
    try:
        if line:
            result = agent_with_memory.invoke({"input":line})
            print(result['output'])
        else:
            break
    except Exception as e:
        print(e)
