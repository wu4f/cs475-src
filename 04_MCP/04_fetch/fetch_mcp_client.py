import asyncio
import os
from fast_agent.core.fastagent import FastAgent

fast = FastAgent("Fetch Agent")

@fast.agent(
    instruction = f"You are a web assistant.  Attempt to answer the user's question via retrieving content from the web.",
    model = "gpt-4.1",
    servers = ["fetch"],
    use_history = True,
)

async def main():
    async with fast.run() as agent:
        await agent.interactive()

if __name__ == "__main__":
    asyncio.run(main())
