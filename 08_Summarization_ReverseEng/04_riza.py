import os
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_community.tools.riza import command
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
llm = ChatGoogleGenerativeAI(model=os.getenv("GOOGLE_MODEL"))
#from langchain_openai import ChatOpenAI
#llm = ChatOpenAI(model=os.getenv("OPENAI_MODEL"))
#from langchain_anthropic import ChatAnthropic
#llm = ChatAnthropic(model=os.getenv("ANTHROPIC_MODEL"))
#from langchain_openai import ChatOpenAI
#llm = ChatOpenAI(model="o3-mini", reasoning_effort="high")

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are an expert at reverse engineering malware.  Use the tools you are given to execute the given code."),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)
tools = [command.ExecPython(), command.ExecJavaScript()]
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

print("Welcome to my Riza application! These are some of my custom tools:")
for tool in tools:
    print(f"  Tool: {tool.name} = {tool.description}")

print("Paste a code snippet and I'll use Riza to analyze what it does.  A blank line exits.")
while True:
    try:
        line = input("llm>> ")
        if line:
            result = agent_executor.invoke({"input": line})
            print(result["output"])
        else:
            break
    except Exception as e:
        print(e)
