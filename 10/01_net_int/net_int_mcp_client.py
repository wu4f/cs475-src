import asyncio
import os
from mcp_agent.core.fastagent import FastAgent

fast = FastAgent("Network Inteligence Agent")

@fast.agent(
    instruction = f"You are an IP address assistant.  Attempt to answer the user's question about an IP address.",
    model = "gpt-4.1",
    servers = ["net_int"],
    use_history = True,
)

async def main():
    async with fast.run() as agent:
        await agent.interactive()

if __name__ == "__main__":
    asyncio.run(main())
