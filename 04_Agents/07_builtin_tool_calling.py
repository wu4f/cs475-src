from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_google_vertexai import ChatVertexAI
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.tools import tool
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

response = llm_with_tools.invoke(query)

print(response.tool_calls)
