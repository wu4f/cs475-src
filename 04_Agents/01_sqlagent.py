from langchain.agents import create_sql_agent
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain_google_genai import GoogleGenerativeAI
from langchain.agents import AgentExecutor
import readline
import sys

database = sys.argv[1]
llm = GoogleGenerativeAI(model="gemini-pro",temperature=0)
db = SQLDatabase.from_uri(f"sqlite:///{database}")
toolkit = SQLDatabaseToolkit(db=db,llm=llm)
agent_executor = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True
)

print(f"Welcome to my database querying application. Tell me what you want")
print(f"from your database at {database}.")

while True:
    try:
        line = input("llm>> ")
        if line:
            result = agent_executor.invoke(line)
            print(result)
        else:
            break
    except:
        break
