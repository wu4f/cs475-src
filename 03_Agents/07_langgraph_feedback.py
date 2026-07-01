import os
import subprocess
from typing import Literal

from langgraph.graph import StateGraph, MessagesState, END
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver

from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langchain_core.tools import tool
from langchain_experimental.tools import PythonREPLTool

# -------------------------
# Tools
# -------------------------
@tool
def execute_command(command: str) -> str:
    """Executes a shell command and returns the output."""
    result = subprocess.run(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if result.returncode == 0:
        return result.stdout
    return f"Error:\n{result.stderr}"

python_repl = PythonREPLTool()
tools = [execute_command, python_repl]
tool_node = ToolNode(tools)

# -------------------------
# LLM
# -------------------------
from langchain_google_genai import ChatGoogleGenerativeAI, HarmCategory, HarmBlockThreshold
llm = ChatGoogleGenerativeAI(
    model=os.getenv("GOOGLE_MODEL"),
    safety_settings={
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE
    },
).bind_tools(tools)
#from langchain_anthropic import ChatAnthropic                                  
#llm = ChatAnthropic(model=os.getenv("ANTHROPIC_MODEL")).bind_tools(tools)      
#from langchain_openai import ChatOpenAI                                        
#llm = ChatOpenAI(model=os.getenv("OPENAI_MODEL")).bind_tools(tools)

# -------------------------
# Graph nodes
# -------------------------
def call_model(state: MessagesState):
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

def human_review_node(state: MessagesState):
    """
    No message to return.  Execution pauses here due to interrupt_before.
    """
    return {}

# -------------------------
# Routing
# -------------------------
def route_after_call(state: MessagesState) -> Literal["human_review", END]:
    last = state["messages"][-1]
    if isinstance(last, AIMessage) and last.tool_calls:
        return "human_review"
    return END


def route_after_human(state: MessagesState) -> Literal["tools", "call"]:
    """
    If the last message is still an AI tool call → user approved → execute tool.
    Otherwise → go back to model.
    """
    last = state["messages"][-1]
    if isinstance(last, AIMessage) and last.tool_calls:
        return "tools"
    return "call"

# -------------------------
# Build workflow
# -------------------------

workflow = StateGraph(MessagesState)

workflow.add_node("call", call_model)
workflow.add_node("human_review", human_review_node)
workflow.add_node("tools", tool_node)

workflow.set_entry_point("call")

workflow.add_conditional_edges("call", route_after_call)
workflow.add_conditional_edges("human_review", route_after_human)

workflow.add_edge("tools", "call")

app = workflow.compile(
    checkpointer=MemorySaver(),
    interrupt_before=["human_review"],
)

# -------------------------
# Human feedback handler
# -------------------------
def get_feedback(app, thread):
    state = app.get_state(thread)
    last = state.values["messages"][-1]

    tool_call = last.tool_calls[0]
    tool_call_id = tool_call["id"]
    tool_name = tool_call["name"]

    user_response = input(
        "\nPress 'y' to approve the tool call\n"
        "or describe how it should be changed:\n> "
    )

    if user_response.strip().lower() == "y":
        return

    feedback = ToolMessage(
        content=f"User requested changes: {user_response}",
        tool_call_id=tool_call_id,
        name=tool_name,
    )

    app.update_state(
        thread,
        {"messages": [feedback]},
        as_node="human_review",
    )


# -------------------------
# REPL loop
# -------------------------

thread = {"configurable": {"thread_id": "1"}}

print('This application implements a human-in-the-loop tool calling application using a Linux shell tool and a Python REPL tool.  Ask the application to perform a task and it will generate a command or code to complete it.  It will then ask you to either confirm execution of it or provide feedback to modify what was generated.  A blank line exits the program.')

while True:
    user_input = input("\n>> ")
    if not user_input:
        break

    inputs = [HumanMessage(content=user_input)]

    for event in app.stream({"messages": inputs}, thread, stream_mode="values"):
        event["messages"][-1].pretty_print()

    while app.get_state(thread).next:
        get_feedback(app, thread)

        for event in app.stream(None, thread, stream_mode="values"):
            event["messages"][-1].pretty_print()

