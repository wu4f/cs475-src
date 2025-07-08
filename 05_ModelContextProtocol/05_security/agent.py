import asyncio
from mcp_agent.core.fastagent import FastAgent

# Create the application
fast = FastAgent("Vulnerability Agent")

model = input("Enter the model to use (default: opus4): ") or "opus4"

@fast.agent(
    instruction=f"You are a vulnerability discovery assistant. Your task is to discover vulnerabilities in systems using the tools provided. Enumerate services on machines to find vulnerable services.",
    model=model,
    servers=["nmap", "opencve", "nuclei", "metasploit", "gobuster", "sqlmap", "curl", "filesystem", "hashcat"],
    use_history=True,
)
async def main():
    async with fast.run() as agent:
        await agent.interactive()


if __name__ == "__main__":
    asyncio.run(main())
