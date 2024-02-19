from langchain.agents import create_sql_agent
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain_google_genai import GoogleGenerativeAI
from langchain.agents import AgentExecutor
import os

llm = GoogleGenerativeAI(model="gemini-pro",temperature=0)
db = SQLDatabase.from_uri("sqlite:///db/roadrecon.db")
toolkit = SQLDatabaseToolkit(db=db,llm=llm)
agent_executor = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True
)
#agent_executor.invoke("List all tables")
#agent_executor.invoke("First, find the table with contact information. Then list the first 100 street addresses")
#agent_executor.invoke("First, find the table with contact information.  Then, list the people who live on 'North Service Road'")
agent_executor.invoke("What Service Principals have AD Roles?")
#agent_executor.invoke("First, find the tables containing service principals and role assignments.  Then, query the role assignments table to find the names of service principals with AD Roles.")
#agent_executor.invoke("Find the user types in this database.")
