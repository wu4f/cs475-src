import asyncio
from mcp_agent.core.fastagent import FastAgent

fast = FastAgent("Network Inteligence Agent")

@fast.agent(
    instruction = f"You are a DNS address assistant.  Attempt to answer the user's question about a DNS address.",
    model = "gpt-4.1",
    servers = ["dns_int"],
    use_history = True,
)

async def main():
    async with fast.run() as agent:
        await agent.interactive()

if __name__ == "__main__":
    asyncio.run(main())