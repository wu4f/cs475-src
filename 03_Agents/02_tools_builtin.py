from langchain import hub
from langchain.agents import load_tools
from langchain.agents import AgentExecutor, create_react_agent
from langchain_google_genai import GoogleGenerativeAI
llm = GoogleGenerativeAI(model="gemini-pro")

tools = load_tools(["serpapi", "llm-math","wikipedia","terminal"], llm=llm)
print(f"Welcome to my application.  I am configured with these tools")
for tool in tools:
  print(f'  Tool: {tool.name} = {tool.description}')

input("Press return to continue:")
print("I am configured with the following prompt:")
print("==========================================")
prompt = hub.pull("hwchase17/react")
print(prompt.template)
print("==========================================")

agent = create_react_agent(llm,tools,prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

print("Type a prompt and I will see if I can help you with it.")

while True:
    try:
        line = input("llm>> ")
        if line:
            result = agent_executor.invoke({"input":line})
            print(result)
        else:
            break
    except:
        break
