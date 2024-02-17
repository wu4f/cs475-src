## Changes from V1
The prompt comes from LangChain hub at https://smith.langchain.com/hub/hwchase17/react

Modified the original agent creation function: initialize_agent to create_react_agent
  - initialize_agent is deprecated as of 0.1.0
  - Now functions have slightly different flow

Added nest_asyncio to fix issues arising occasionally from asyncio loop
