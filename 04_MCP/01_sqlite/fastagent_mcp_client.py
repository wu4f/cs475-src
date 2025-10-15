import asyncio
import sys
from fast_agent.core.fastagent import FastAgent
from fast_agent.llm.model_factory import ModelFactory
from fast_agent.llm.provider_types import Provider
import questionary

# Create the application
fast = FastAgent("SQLite Agent")

@fast.agent(
    instruction=f"You are a Sqlite3 database look up tool. Perform queries on the database given the user's input.  Utilize the user input verbatim when sending the query to the database and print the query that was sent to the database",
    model="gpt-4.1",
    servers=["vulnerable_sqlite_stdio"],
    use_history=True,
)
async def main():
    async with fast.run() as agent:
        await agent.interactive()

if __name__ == "__main__":
    asyncio.run(main())
