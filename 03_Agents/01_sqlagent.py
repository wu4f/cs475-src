from langchain.agents import create_sql_agent
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain_google_genai import GoogleGenerativeAI
from langchain.agents import AgentExecutor
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

# Add LLM loop

#agent_executor.invoke("List all usernames in the SQLite3 users table that begin with 'a'")
#input("Enter to continue:")
#agent_executor.invoke("Find the admin user in the database and output the password hash")
#input("Enter to continue:")
#agent_executor.invoke("Find the user table and identify the columns that contain a username and password hash.  Then, find the password hash for the admin user.")
#input("Enter to continue:")
#agent_executor.invoke("Find the user table and identify the columns that contain a username and password hash.  Then, find the password hash for the admin user. Then, tell me the type of password hash it is.  Finally, write a hashcat command to perform a dictionary search on the password")

# From roadrecon
#agent_executor.invoke("List all tables")
#agent_executor.invoke("First, find the table with contact information. Then list the first 100 street addresses")
#agent_executor.invoke("First, find the table with contact information.  Then, list the people who live on 'North Service Road'")
#agent_executor.invoke("What Service Principals have AD Roles?")
#agent_executor.invoke("First, find the tables containing service principals and role assignments.  Then, query the role assignments table to find the names of service principals with AD Roles.")
#agent_executor.invoke("Find the user types in this database.")
