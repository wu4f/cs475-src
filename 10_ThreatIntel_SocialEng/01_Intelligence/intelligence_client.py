import asyncio
from fast_agent.core.fastagent import FastAgent
from fast_agent.llm.model_factory import ModelFactory
from fast_agent.llm.provider_types import Provider
import questionary

# Create the application
fast = FastAgent("Inteligence Agent")

choices = []
for model in ModelFactory.DEFAULT_PROVIDERS:
    if ModelFactory.DEFAULT_PROVIDERS[model] == Provider.FAST_AGENT:
        continue
    choices.append(model)

choices.append("custom")

model = questionary.select(
    "Select the model to use for the agent:",
    choices=choices,
).ask()

if model == "custom":
    model = questionary.text(
        "Enter the model name (e.g., 'openai.gpt-4o', 'openai.gpt-4.1', etc.):"
    ).ask()

tools = []
for tool in fast.config["mcp"]["servers"]:
    tools.append(tool)

tools = questionary.checkbox(
    "Select the tools to use for the agent:",
    choices=tools,
).ask()

@fast.agent(
    instruction = f"You are an intelligence agent.  Attempt to answer the user's questions using the tools you have access to.",
    model=model,
    servers=tools,
    use_history=True,
)

async def main():
    async with fast.run() as agent:
        await agent.interactive()

if __name__ == "__main__":
    asyncio.run(main())
