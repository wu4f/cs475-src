from langchain import hub
from langchain_chroma import Chroma
from langchain.agents import AgentExecutor, create_react_agent
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain.tools import tool
from pydantic import BaseModel, Field
from langchain_google_genai import GoogleGenerativeAI,GoogleGenerativeAIEmbeddings, HarmCategory, HarmBlockThreshold
import readline
import os
#import langchain
#langchain.debug = True

llm = GoogleGenerativeAI( model="gemini-pro", temperature=0, safety_settings = { HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE, })

vectorstore = Chroma(
     persist_directory="./rag_data/.chromadb",
     embedding_function=GoogleGenerativeAIEmbeddings(model="models/embedding-001", task_type="retrieval_query")
)

retriever = vectorstore.as_retriever()

def format_docs(docs):
    return docs[0].page_content

rag_chain = (
    retriever | format_docs
)

class SearchInput(BaseModel):
    query: str = Field(description="should be a plain text summary of the users prompt, preserving the main idea")

@tool("vector_db_query", args_schema=SearchInput ,return_direct=False)
def vector_db_query(query: str) -> str:
	"""Can look up specific information using plain text questions"""
	# Put chromadb look up tool here	
	rag_result = rag_chain.invoke(query)	
	print(f"rag result is: {rag_result}")
	return rag_result

tools = load_tools(["terminal"], allow_dangerous_tools=True)
tools.extend([vector_db_query])

base_prompt = hub.pull("langchain-ai/react-agent-template")
#base_prompt.pretty_print()
prompt = base_prompt.partial(instructions="Answer the user's request utilizing at most 8 tool calls")
#prompt.pretty_print()

agent = create_react_agent(llm,tools,prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

print("Welcome to my application. I am configured with these tools:")
for tool in agent_executor.tools:
  print(f'  Tool: {tool.name} Description: {tool.description}')

while True:
    line = input("llm>> ")
    try:
        if line:
            result = agent_executor.invoke({"input":line})
            print(result)
        else:
            break
    except Exception as e:
        print(e)
