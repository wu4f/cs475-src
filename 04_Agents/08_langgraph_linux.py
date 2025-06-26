import os 
import readline
from langgraph.graph import Graph, END, START
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

# Create nodes
def linux_command_node(user_input):
    response = llm.invoke(
        f"""Given the user's prompt, you are to generate a Linux command to answer it. Provide no other formatting, just the command. \n\n  User prompt: {user_input}"""
    )
    return response.content if hasattr(response, 'content') else response


def user_check(linux_command):
    print(f"Linux command is: {linux_command}")
    user_ack = input("Should I execute this command? ")
    response = llm.invoke(
        f"""The following is the response the user gave to 'Should I execute this command?': {user_ack} \n\n  If the answer given is a negative one, return NO else return YES"""
    )
    response_text = response.content if hasattr(response, 'content') else response
    if 'YES' in response_text:
        return 'linux_node'
    else:
        return END


def linux_node(linux_command):
    result = os.system(linux_command)
    return END

# Define graph
workflow = Graph()
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
            result = app.invoke(line)
            print(result)
        else:
            break
    except Exception as e:
        print(e)
