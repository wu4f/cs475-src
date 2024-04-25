from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent, load_tools
from langchain.tools import tool
from langchain_core.pydantic_v1 import BaseModel, Field, root_validator
from langchain_google_genai import GoogleGenerativeAI, HarmCategory, HarmBlockThreshold
import dns.resolver, dns.reversename
import validators
import readline
import os

#from langsmith import Client
#os.environ["LANGCHAIN_TRACING_V2"] = "true"
#os.environ["LANGCHAIN_PROJECT"] = f"LangSmith Introduction"
#os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
#client = Client()
llm = GoogleGenerativeAI(
           model="gemini-1.5-pro-latest",
           temperature=0,
           safety_settings = { HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE, }
)

class LookupNameInput(BaseModel):
    hostname: str = Field(description="Should be a hostname such as www.google.com")
    @root_validator
    def is_dns_address(cls, values: dict[str,any]) -> str:
        if validators.domain(values.get("hostname")):
            return values
        raise ValueError("Malformed hostname")

@tool("lookup_name",args_schema=LookupNameInput, return_direct=False)
def lookup_name(hostname):
    """Given a DNS hostname, it will return its IPv4 addresses"""
    result = dns.resolver.resolve(hostname, 'A')
    res = [ r.to_text() for r in result ]
    return res[0]

class LookupIPInput(BaseModel):
    address: str = Field(description="Should be an IP address such as 208.91.197.27 or 143.95.239.83")
    @root_validator
    def is_ip_address(cls, values: dict[str,any]) -> str:
        if validators.ip_address.ipv4(values.get("address")):
            return values
        raise ValueError("Malformed IP address")

@tool("lookup_ip", args_schema=LookupIPInput, return_direct=False)
def lookup_ip(address):
    """Given an IP address, returns names associated with it"""
    n = dns.reversename.from_address(address)
    result = dns.resolver.resolve(n, 'PTR')
    res = [ r.to_text() for r in result ]
    return res[0]
    
tools = load_tools(["serpapi", "terminal"], allow_dangerous_tools=True)
tools.extend([lookup_name, lookup_ip])

base_prompt = hub.pull("langchain-ai/react-agent-template")
prompt = base_prompt.partial(instructions="Answer the user's request utilizing at most 8 tool calls")

agent = create_react_agent(llm,tools,prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

print("Welcome to my application. I am configured with these tools:")
for tool in agent_executor.tools:
  print(f'  Tool: {tool.name} = {tool.description}')

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
