import asyncio
from mcp_agent.core.fastagent import FastAgent

fast = FastAgent("Command Agent")

@fast.agent(
    instruction = f"You are a Linux command agent.  Generate a command based on the user's request and return the results of execution directly back.",
    model = "gpt-4.1",
    servers = ["command"],
    use_history = True
)

async def main():
    async with fast.run() as agent:
        await agent.interactive()

if __name__ == "__main__":
    asyncio.run(main())
