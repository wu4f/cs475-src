import os 
import readline
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, END, START
from langchain_google_genai import ChatGoogleGenerativeAI, HarmCategory, HarmBlockThreshold
llm = ChatGoogleGenerativeAI(
    model=os.getenv("GOOGLE_MODEL"),
    safety_settings={
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE
    }
)
#from langchain_openai import ChatOpenAI
#llm = ChatOpenAI(model=os.getenv("OPENAI_MODEL"))
#from langchain_anthropic import ChatAnthropic
#llm = ChatAnthropic(model=os.getenv("ANTHROPIC_MODEL"))

class AgentState(TypedDict):
    messages: list

# Create nodes
def linux_command_node(state: AgentState):
    user_input = state["messages"][-1]

    response = llm.invoke(
        f"""Given the user's prompt, generate a Linux command.  Provide no formatting, only the command. \n\n User prompt: {user_input}"""
    )

    command = response.content if hasattr(response, "content") else response
    return {"messages": state["messages"] + [command]}

def user_check(state: AgentState):
    linux_command = state["messages"][-1]
    print(f"Linux command is: {linux_command}")

    user_ack = input("Should I execute this command? ")

    response = llm.invoke(
        f"""The following is the response the user gave to 'Should I execute this command?': {user_ack} \n\n If the answer is negative, return NO. Otherwise return YES."""
    )

    response_text = response.content if hasattr(response, "content") else response
    return "linux_node" if "YES" in response_text else END

def linux_node(state: AgentState):
    linux_command = state["messages"][-1]
    os.system(linux_command)
    return state

# Define graph
workflow = StateGraph(AgentState)
workflow.add_node("linux_command_node", linux_command_node)
workflow.add_node("linux_node", linux_node)

workflow.add_edge(START, "linux_command_node")
workflow.add_conditional_edges(
    'linux_command_node', user_check
)
workflow.add_edge('linux_node', END)

app = workflow.compile()

print("Welcome to my human-in-the-loop Linux command-line tool.  Ask me to do perform a task and I will generate and execute it in the shell.  A blank line exits.")
while True:
    line = input(">> ")
    try:
        if line:
            result = app.invoke({"messages": [line]})
            print(result)
        else:
            break
    except Exception as e:
        print(e)

