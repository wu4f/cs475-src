from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_google_vertexai import ChatVertexAI
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage
import getpass
import os
import google.auth

@tool
def add(a: int, b: int) -> int:
    """Adds a and b."""
    return a + b


@tool
def multiply(a: int, b: int) -> int:
    """Multiplies a and b."""
    return a * b


tools = [add, multiply]

# os.environ["GOOGLE_API_KEY"] = getpass.getpass()

llm = ChatVertexAI(model="gemini-pro")
llm_with_tools = llm.bind_tools(tools)

query = "What is 3 * 12? Also, what is 11 + 49?"

# response = llm_with_tools.invoke(query)

messages = [HumanMessage(query)]

while True:
    ai_msg = llm_with_tools.invoke(messages)
    messages.append(ai_msg)

    print(f"Here is the ai message in response to llm_with_tools.invoke(messages):\n {ai_msg.tool_calls}")

    if len(ai_msg.tool_calls) == 0:
        print(f"The final message is {ai_msg}")
        break

    for tool_call in ai_msg.tool_calls:
        selected_tool = {"add": add, "multiply": multiply}[tool_call["name"].lower()]
        tool_output = selected_tool.invoke(tool_call["args"])
        print(f"The tool output is: {tool_output}")
        messages.append(ToolMessage(tool_output, tool_call_id=tool_call["id"]))

    # print(messages)

