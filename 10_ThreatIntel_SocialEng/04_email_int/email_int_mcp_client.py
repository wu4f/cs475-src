import asyncio
from mcp_agent.core.fastagent import FastAgent

fast = FastAgent("Email Inteligence Agent")

@fast.agent(
    instruction = f"You are an Email analyzer.  Attempt to answer the user's question about an e-mail address.",
    model = "gpt-4.1",
    servers = ["email_int"],
    use_history = True,
)

async def main():
    async with fast.run() as agent:
        await agent.interactive()

if __name__ == "__main__":
    asyncio.run(main())