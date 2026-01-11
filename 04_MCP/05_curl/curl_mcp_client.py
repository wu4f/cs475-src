import asyncio
from fast_agent.core.fastagent import FastAgent
import readline

fast = FastAgent("Curl Agent")

model = input("Enter the model to use (default: opus4): ") or "opus4"

@fast.agent(
    instruction=f"You are a web access assistant. Your task is to access web sites using the curl command to answer a user's questions",
    model=model,
    servers=["curl"],
    use_history=True,
)
async def main():
    async with fast.run() as agent:
        await agent.interactive()

if __name__ == "__main__":
    asyncio.run(main())
