import asyncio
from mcp_agent.core.fastagent import FastAgent

fast = FastAgent("App Inteligence Agent")

@fast.agent(
    instruction = f"You are an assistant providing information on CVEs and CWEs. Attempt to answer the user's question about particular ones.",
    model = "gpt-4.1",
    servers = ["app_int"],
    use_history = True,
)

async def main():
    async with fast.run() as agent:
        await agent.interactive()

if __name__ == "__main__":
    asyncio.run(main())