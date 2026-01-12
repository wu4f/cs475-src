import asyncio
from fast_agent.core.fastagent import FastAgent

# Create the application
fast = FastAgent("SQLite Agent")

@fast.agent(
    instruction=f"You are a Sqlite3 database look up tool. Perform queries on the database given the user's input.  Utilize the user input verbatim when sending the query to the database and print the query that was sent to the database",
    model="gemini2", # Alternates at https://fast-agent.ai/models/llm_providers
    servers=["sqlite_stdio"],
    use_history=True,
)
async def main():
    async with fast.run() as agent:
        await agent.interactive()

if __name__ == "__main__":
    asyncio.run(main())
