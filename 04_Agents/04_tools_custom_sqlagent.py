from langchain.agents import create_sql_agent
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain_google_genai import GoogleGenerativeAI, HarmCategory, HarmBlockThreshold
from langchain.tools import Tool
from langchain.agents import AgentExecutor
import readline
import ast
import json
import sys

def fetch_users_pass(user):
   res = db.run(f"SELECT passhash FROM users WHERE username = '{user}';")
   result = [el for sub in ast.literal_eval(res) for el in sub]
   return result

fetch_users_pass_tool = Tool.from_function(
  func=fetch_users_pass,
  name="FetchUsersPass",
  description="Useful when you want to fetch a password hash for a particular user.  Takes a username as an argument."
)

def fetch_users(query):
   res = db.run("SELECT username FROM users;")
   result = [el for sub in ast.literal_eval(res) for el in sub]
   return json.dumps(result)

fetch_users_tool = Tool.from_function(
  func=fetch_users,
  name="FetchUsers",
  description="Useful when you want to fetch the users in the database.  Takes no arguments"
)

database = sys.argv[1]
llm = GoogleGenerativeAI(
             model="gemini-pro",
             temperature=0,
             safety_settings = {
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
             }
      )
db = SQLDatabase.from_uri(f"sqlite:///{database}")
toolkit = SQLDatabaseToolkit(db=db,llm=llm)
agent_executor = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    extra_tools=[fetch_users_tool, fetch_users_pass_tool],
    verbose=True
)

print(f"Welcome to my database querying application.  I've loaded your database at {database} and I am configured with these tools:")
for tool in agent_executor.tools:
  print(f'  Tool: {tool.name} = {tool.description}')

while True:
    line = input("llm>> ")
    if line:
        try:
            result = agent_executor.invoke(line)
            print(result)
        except Exception as e:
            print(e)
    else:
        break
