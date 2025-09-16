import os
import readline
import validators
import dns.resolver, dns.reversename
from pydantic import BaseModel, Field, model_validator
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain.tools import tool
#from langsmith import Client
#os.environ["LANGCHAIN_TRACING_V2"] = "true"
#os.environ["LANGCHAIN_PROJECT"] = f"LangSmith Introduction"
#os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
#client = Client()
from langchain_google_genai import ChatGoogleGenerativeAI, HarmCategory, HarmBlockThreshold
llm = ChatGoogleGenerativeAI(
           model=os.getenv("GOOGLE_MODEL"),
           safety_settings = { HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE, }
)
#from langchain_openai import ChatOpenAI
#llm = ChatOpenAI(model=os.getenv("OPENAI_MODEL"))
#from langchain_anthropic import ChatAnthropic
#llm = ChatAnthropic(model=os.getenv("ANTHROPIC_MODEL"))

class LookupNameInput(BaseModel):
    hostname: str = Field(description="Should be a hostname such as www.google.com")
    @model_validator(mode="before")
    def is_dns_address(cls, values: dict[str,any]) -> dict[str,any]:
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
    @model_validator(mode="before")
    def is_ip_address(cls, values: dict[str,any]) -> dict[str,any]:
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
    
tools = load_tools([])
tools.extend([lookup_name, lookup_ip])

base_prompt = hub.pull("langchain-ai/react-agent-template")
prompt = base_prompt.partial(instructions="Answer the user's request utilizing at most 8 tool calls")

agent = create_react_agent(llm,tools,prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

print("Welcome to my DNS and IP address lookup application. I am configured with these tools:")
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
