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


#agent_executor.invoke({"input":"List the files in my current directory."})
#agent_executor.invoke({"input":"Explain what synesthesia is."})
#agent_executor.invoke({"input":"Find me a recipe for Boston Creme Pie."})
#agent_executor.invoke({"input":"How much money do I have if I take 10,000 dollars and compound it annually by 5 percent for 20 years?"})
#agent_executor.invoke({"input":"Can you summarize this URL? https://krebsonsecurity.com/2024/02/arrests-in-400m-sim-swap-tied-to-heist-at-ftx/.  What is the main security issue it talks about?"})
#agent_executor.invoke({"input":"What percent of electricity is consumed by data centers in the US"})
