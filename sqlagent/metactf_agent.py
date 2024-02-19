from langchain.agents import create_sql_agent
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain_google_genai import GoogleGenerativeAI
from langchain.agents import AgentExecutor
import os

llm = GoogleGenerativeAI(model="gemini-pro",temperature=0)
db = SQLDatabase.from_uri("sqlite:///db/metactf_users.db")
toolkit = SQLDatabaseToolkit(db=db,llm=llm)
agent_executor = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True
)
#agent_executor.invoke("List all usernames in the SQLite3 users table that begin with 'a'")
#input("Enter to continue:")
#agent_executor.invoke("Find the admin user in the database and output the password hash")
#input("Enter to continue:")
#agent_executor.invoke("Find the user table and identify the columns that contain a username and password hash.  Then, find the password hash for the admin user.")
#input("Enter to continue:")
agent_executor.invoke("Find the user table and identify the columns that contain a username and password hash.  Then, find the password hash for the admin user. Then, tell me the type of password hash it is.  Finally, write a hashcat command to perform a dictionary search on the password")
