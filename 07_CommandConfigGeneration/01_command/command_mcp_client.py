import asyncio
from fast_agent.core.fastagent import FastAgent
import sys

user_instructions = sys.argv[1]

fast = FastAgent("Command Agent")

@fast.agent(
    instruction = user_instructions,
    model = "gemini25",
    servers = ["command"],
    use_history = True
)

async def main():
    async with fast.run() as agent:
        await agent.interactive()

if __name__ == "__main__":
    asyncio.run(main())
