from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain_experimental.tools import PythonREPLTool
from langchain_google_genai import ChatGoogleGenerativeAI
import readline
tools = [PythonREPLTool()]

llm = ChatGoogleGenerativeAI(model="gemini-pro",temperature=0)

instructions = """You are an agent designed to write and execute python code to answer questions.
You have access to a python REPL, which you can use to execute python code.
If you get an error, debug your code and try again.
Only use the output of your code to answer the question. 
You might know the answer without running any code, but you should still run the code to get the answer.
If it does not seem like you can write code to answer the question, just return "I don't know" as the answer.
"""
base_prompt = hub.pull("langchain-ai/react-agent-template")
prompt = base_prompt.partial(instructions=instructions)

agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

#agent_executor.invoke({"input":"What is the 10th fibonacci number?"})
#agent_executor.invoke({"input":"Sort this list of numbers: [10, 5, 8, 3, 9]"})
#agent_executor.invoke({"input":"What is the 5th smallest prime number?"})

while True:
    line = input("llm>> ")
    if line:
        print(agent_executor.invoke({"input":line}))
    else:
        break
