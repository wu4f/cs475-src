import asyncio
from mcp_agent.core.fastagent import FastAgent

fast = FastAgent("Authentication Breaker Agent")

@fast.agent(
    instruction = f"You are a brute-force credential stuffer.  Attempt to answer the user's question about logging into a site.",
    model = "gpt-4.1",
    servers = ["auth_breaker"],
    use_history = True,
)

async def main():
    async with fast.run() as agent:
        await agent.interactive()

if __name__ == "__main__":
    asyncio.run(main())
