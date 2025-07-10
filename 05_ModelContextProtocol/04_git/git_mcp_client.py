import asyncio
import os
from mcp_agent.core.fastagent import FastAgent

# Create the application
fast = FastAgent("Git Agent")


@fast.agent(
    instruction=f"You are a git assistant for the repository located here at {os.path.dirname(os.path.dirname(os.getcwd()))}",
    model="gpt-4.1",
    servers=["git"],
    use_history=True,
)

async def main():
    async with fast.run() as agent:
        await agent.interactive()

if __name__ == "__main__":
    asyncio.run(main())
