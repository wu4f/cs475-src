from msticpy.sectools.tilookup import TILookup
from msticpy.sectools.vtlookupv3.vtlookupv3 import VTLookupV3
from msticpy.common.provider_settings import get_provider_settings
from langchain.agents import Tool, AgentType, AgentExecutor, create_react_agent
from langchain_openai import ChatOpenAI
from langchain import hub
import nest_asyncio

# May solve errors from async_io calls in langchain library
nest_asyncio.apply()

llm = ChatOpenAI(model_name="gpt-4", temperature=0.3)
vt_key = get_provider_settings("TIProviders")["VirusTotal"].args["AuthKey"]
vt_lookup = VTLookupV3(vt_key)

class TIVTLookup:
    def __init__(self):
        self.ti_lookup = TILookup()

    def ip_info(self, ip_address: str) -> str:
        result = self.ti_lookup.lookup_ioc(observable=ip_address, ioc_type="ipv4", providers=["VirusTotal"])
        details = result.at[0, 'RawResult']
        sliced_details = str(details)[:3500]
        return sliced_details

    def communicating_samples(self, ip_address: str) -> str:
        domain_relation = vt_lookup.lookup_ioc_relationships(observable = ip_address, vt_type = 'ip_address', relationship = 'communicating_files', limit = "10")
        return domain_relation

    def samples_identification(self, hash: str) -> str:
        hash_details = vt_lookup.get_object(hash, "file")
        return hash_details

ti_tool = TIVTLookup()

tools = [
    Tool(
        name="Retrieve_IP_Info",
        func=ti_tool.ip_info,
        description="Useful when you need to look up threat intelligence information for an IP address.",
    ),
    Tool(
        name="Retrieve_Communicating_Samples",
        func=ti_tool.communicating_samples,
        description="Useful when you need to get communicating samples from an ip or domain.",
    ),
    Tool(
        name="Retrieve_Sample_information",
        func=ti_tool.samples_identification,
        description="Useful when you need to obtain more details about a sample.",
    ),
]

prompt = hub.pull("hwchase17/react")

agent = create_react_agent(llm,tools,prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

agent_executor.invoke({"input": "Can you give me more details about this ip: 77.246.107.91? How many samples are related to this ip? If you found samples related, can you give me more info about the first one?"})



#agent = initialize_agent(
#    tools, llm=llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
#agent.run("Can you give me more details about this ip: 77.246.107.91? How many samples are related to this ip? If you found samples related, can you give me more info about the first one?")
