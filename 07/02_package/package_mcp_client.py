import asyncio
from mcp_agent.core.fastagent import FastAgent

fast = FastAgent("Package Agent")

@fast.agent(
    instruction = f"You are a package analysis agent.  Use the tools to answer the user's request",
    model = "gpt-4.1",
    servers = ["package"],
    use_history = True,
)

async def main():
    async with fast.run() as agent:
        await agent.interactive()

if __name__ == "__main__":
    asyncio.run(main())
