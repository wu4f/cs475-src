import asyncio
from mcp_agent.core.fastagent import FastAgent

# Create the application
fast = FastAgent("Vulnerability Agent")

@fast.agent(
    instruction=f"You are a vulnerability discovery assistant. Your task is to discover vulnerabilities in systems using the tools provided. Enumerate services on machines to find vulnerable services.",
    model="opus4",
    servers=["nmap", "opencve", "nuclei"],
    use_history=True,
)
async def main():
    async with fast.run() as agent:
        await agent.interactive()


if __name__ == "__main__":
    asyncio.run(main())
