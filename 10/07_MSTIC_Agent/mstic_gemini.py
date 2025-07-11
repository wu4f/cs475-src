from msticpy.sectools.tilookup import TILookup
from msticpy.sectools.vtlookupv3.vtlookupv3 import VTLookupV3
from msticpy.common.provider_settings import get_provider_settings
from langchain import hub
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import Tool
from langchain.agents import AgentExecutor, create_react_agent
#import nest_asyncio
import os
import json
import readline

# May solve errors from async_io calls in langchain library
#nest_asyncio.apply()

llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest", temperature=0.05)

vt_key = get_provider_settings("TIProviders")["VirusTotal"].args["AuthKey"]

vt_lookup = VTLookupV3(vt_key)

class TIVTLookup:
    def __init__(self):
        self.ti_lookup = TILookup()

    def ip_info(self, ip_address: str) -> str:
        result = self.ti_lookup.lookup_ioc(observable=ip_address, ioc_type="ipv4", providers=["VirusTotal"])
        details = result.at[0, 'RawResult']
        comm_samples = details['detected_communicating_samples']
        return json.dumps(comm_samples)

    def samples_identification(self, hash: str) -> str:
        result = vt_lookup.get_object(hash, "file")
        json_result = result.to_json(orient='records')
        return json_result

ti_tool = TIVTLookup()

tools = [
    Tool(
        name="Retrieve_IP_Info",
        func=ti_tool.ip_info,
        description="(CHANGE ME)",
    ),
    Tool(
        name="Retrieve_hash_information",
        func=ti_tool.samples_identification,
        description="(CHANGE ME)",
    ),
]

base_prompt = hub.pull("langchain-ai/react-agent-template")
prompt = base_prompt.partial(instructions="Answer the user's request utilizing at most 5 tool calls")

agent = create_react_agent(llm,tools,prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

def process_query(query):
  response = agent_executor.invoke({"input": query})
  return(response)

print("Welcome to my MSTIC agent.  Enter a query.  An example is below\nCan you give me more details about this ip: 77.246.107.91? How many samples are related to this ip? If you found samples related, can you give me more info about the first one?")
while True:
    line = input("llm>> ")
    if line:
        print(process_query(line.strip()))
    else:
        break
