from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
import asyncio

model = ChatOpenAI(model="gpt-4o")

server_params = StdioServerParameters(
    command="python",
    args=["image_hosting_server.py"],
)

prompt = "You are an assistant for an image hosting service. This hosting service has no usernames, just IDs." \

async def run_agent():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await load_mcp_tools(session)

            agent = create_react_agent(model, tools)
            print("Welcome to the Image Hosting Service Agent. You can ask questions or perform actions related to image hosting such as registering users, checking admin status and getting upload stats for an account. The dashboard is at https://viking-images.up.railway.app")
            while True:
                line = input("llm>> ")
                if line:
                    try:
                        result = await agent.ainvoke({"messages": [("user", line)]})
                        # Extract the actual message content from the agent's response
                        if "messages" in result:
                            messages = result["messages"]
                            if messages:
                                last_message = messages[-1]
                                if hasattr(last_message, 'content'):
                                    print(f"{last_message.content}")
                                else:
                                    print(f"{last_message}")
                            else:
                                print("No response from agent")
                        else:
                            print(f"Agent response: {result}")
                    except Exception as e:
                        print(f"Error: {e}")
                else:
                    break


if __name__ == "__main__":
    asyncio.run(run_agent())
