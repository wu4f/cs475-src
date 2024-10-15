from langchain_google_genai import ChatGoogleGenerativeAI, HarmCategory, HarmBlockThreshold
from langgraph.graph import Graph, END, START
from langchain_core.messages import AIMessage
from typing import Annotated, Literal, TypedDict
from langchain_core.tools import Tool
from langchain_experimental.utilities import PythonREPL
from langchain_experimental.tools import PythonREPLTool
from langgraph.prebuilt import ToolNode
from langchain_community.tools import ShellTool
from langchain_core.messages import HumanMessage
from langgraph.graph import END, StateGraph, MessagesState
from langchain_anthropic import ChatAnthropic
import readline
import os
from langgraph.checkpoint.memory import MemorySaver

#Used to persist memory between graph runs
checkpointer = MemorySaver()


shell_tool = ShellTool()

# Create a python repl tool
python_repl = PythonREPLTool()
tools = [python_repl, shell_tool]

model = ChatAnthropic(model="claude-3-5-sonnet-20240620", temperature=0).bind_tools(tools)
# model = ChatGoogleGenerativeAI( model="gemini-1.5-flash", temperature=0, safety_settings = { HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE, }).bind_tools(tools)

def call_model(state: MessagesState):
    messages = state['messages']
    response = model.invoke(messages)
    # We return a list, because this will get added to the existing list
    return {"messages": [response]}

def human_review_node(state: MessagesState):
  pass

# Use prebuilt tool node component
tool_node = ToolNode(tools)

def route_after_agent(state: MessagesState) -> Literal["human_review_node", END]:
    messages = state['messages']
    last_message = messages[-1]
    # If the LLM makes a tool call, then we route to the "tools" node
    if last_message.tool_calls:
        return "human_review_node"
    # Otherwise, we stop (reply to the user)
    return END

def route_after_human(state: MessagesState) -> Literal["tools", "agent"]:
  messages = state['messages']
  last_message = messages[-1]
  # If the last message in the state is still a tool call after the interupt
  # it means the user authorized the tool call
  if isinstance(state["messages"][-1], AIMessage):
    return "tools"
  else:
    return "agent"
  
def get_feedback(graph, thread):
  state = graph.get_state(thread)
  # Append the tool call here depending on user input
  #if user responds y, dont append tool call
  # if user responds with other response, append that as tool response
  current_content = state.values['messages'][-1].content
  current_id = state.values['messages'][-1].id
  tool_call_id = state.values['messages'][-1].tool_calls[0]['id']
  tool_call_name = state.values['messages'][-1].tool_calls[0]['name']

  user_response = input(f"""Press y if the tool call looks good\n otherwise supply
  an explanation of how you would like to edit the tool call\n""")
  if user_response.strip() == "y":
    return
  else:
    new_message = {
    "role": "tool",
    # This is our natural language feedback
    "content": f"User requested changes: {user_response}",
    "name": tool_call_name,
    "tool_call_id": tool_call_id
    }
    # Update the graph state here
    graph.update_state(
        thread,
        {"messages": [new_message]},
        as_node="human_review_node"
    )
    return
  
workflow = StateGraph(MessagesState)
# Define the nodes
workflow.add_node("agent", call_model)
workflow.add_node("human_review_node", human_review_node)
workflow.add_node("tools", tool_node)

# Set the entrypoint as `agent`
# This means that this node is the first one called
workflow.set_entry_point("agent")
# We now add a conditional edge
workflow.add_conditional_edges(
    # First, we define the start node. We use `agent`.
    # This means these are the edges taken after the `agent` node is called.
    "agent",
    # Next, we pass in the function that will determine which node is called next.
    route_after_agent
)

workflow.add_conditional_edges(
    "human_review_node",
    route_after_human
)

# We now add a normal edge from `tools` to `agent`.
# This means that after `tools` is called, `agent` node is called next.
workflow.add_edge("tools", 'agent')

app = workflow.compile(checkpointer=checkpointer, interrupt_before=["human_review_node"])
thread = {"configurable": {"thread_id": "14"}}

keep_going=True
while keep_going:

  user_input = input("User> ")
  if not user_input:
    break
  inputs = [HumanMessage(content=user_input)]
  for event in app.stream({"messages": inputs}, thread, stream_mode="values"):
    event["messages"][-1].pretty_print()
  if len(app.get_state(thread).next) == 0:
    # The graph has finished executing
    # we want to go back to the start
    pass
  else:
    # A tool call may generate another tool call
    # so a loop is needed
    while True:
      # There is a tool call, we will call our feedback function
      get_feedback(app, thread)
      # In the get feed back function we decided if we should modify the graph state
      for event in app.stream(None, thread, stream_mode="values"):
        event["messages"][-1].pretty_print()
      if len(app.get_state(thread).next) == 0:
        # The graph has finished executing
        # we want to go back to the start
        break