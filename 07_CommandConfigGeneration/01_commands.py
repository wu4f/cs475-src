from langchain_google_genai import GoogleGenerativeAI
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent, load_tools
import readline

llm = GoogleGenerativeAI(model="gemini-1.5-pro-latest",temperature=0)

tools = load_tools(["terminal"], llm=llm, allow_dangerous_tools=True)
base_prompt = hub.pull("langchain-ai/react-agent-template")
prompt = base_prompt.partial(instructions="Answer the user's request by running Linux, gcloud, and terraform commands via the Terminal tool.")
agent = create_react_agent(llm,tools,prompt)
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
