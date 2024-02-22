from langchain import hub
from langchain.agents import load_tools
from langchain.agents import AgentExecutor, create_react_agent
from langchain_google_genai import GoogleGenerativeAI
llm = GoogleGenerativeAI(model="gemini-pro")

#Tools are functions that agents can use to interact with the world.
#The tools the agent will have access to are: [Google search, math, wikipedia, terminal]
tools = load_tools(["serpapi", "llm-math","wikipedia","terminal"], llm=llm)
prompt = hub.pull("hwchase17/react")
agent = create_react_agent(llm,tools,prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
#agent_executor.invoke({"input":"List the files in my current directory."})
#agent_executor.invoke({"input":"Explain what synesthesia is."})
#agent_executor.invoke({"input":"Find me a recipe for Boston Creme Pie."})
#agent_executor.invoke({"input":"How much money do I have if I take 10,000 dollars and compound it annually by 5 percent for 20 years?"})
#agent_executor.invoke({"input":"Can you summarize this URL? https://krebsonsecurity.com/2024/02/arrests-in-400m-sim-swap-tied-to-heist-at-ftx/.  What is the main security issue it talks about?"})
agent_executor.invoke({"input":"What percent of electricity is consumed by data centers in the US"})
