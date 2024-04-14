from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain_experimental.tools import PythonREPLTool
from langchain_google_genai import GoogleGenerativeAI
import readline
tools = [PythonREPLTool()]

# For those wanting to use OpenAI:
#  from langchain_openai import ChatOpenAI
#  llm = ChatOpenAI(model_name="gpt-4-turbo")
llm = GoogleGenerativeAI(model="gemini-pro",temperature=0)

instructions = """You are an agent designed to write and execute python code to
answer questions.  You have access to a python REPL, which you can use to execute
python code.  If you get an error, debug your code and try again.  Only use the
output of your code to answer the question.  You might know the answer without
running any code, but you should still run the code to get the answer.  If it does
not seem like you can write code to answer the question, just return "I don't know"
as the answer.
"""
base_prompt = hub.pull("langchain-ai/react-agent-template")
prompt = base_prompt.partial(instructions=instructions)

agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

print(f"Welcome to my application.  I am configured with these tools")
for tool in tools:
  print(f'  Tool: {tool.name} = {tool.description}')

while True:
    try:
        line = input("llm>> ")
        if line:
            result = agent_executor.invoke({"input":line})
            print(result)
        else:
            break
    except Exception as e:
        print(e)
