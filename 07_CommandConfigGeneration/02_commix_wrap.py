from langchain_google_genai import GoogleGenerativeAI, HarmCategory, HarmBlockThreshold
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent, load_tools
from langchain.tools import BaseTool, StructuredTool, tool
from langchain.pydantic_v1 import BaseModel, Field
import readline
import subprocess
import pexpect
import sys
import select
import threading

command_line_injections="code refactoring for website"

llm = GoogleGenerativeAI(
    model="gemini-1.5-pro-latest",
    temperature=0,
    safety_settings = { HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE, }
    )

def read_output(proc):
    try:
        while True:
            # Read and print all available output from the process
            output = proc.read_nonblocking(size=1024, timeout=60)
            if output:
                print(output.decode(), end='')
    except pexpect.EOF:
        pass
    except Exception as e:
        print(f"Error reading output: {e}")

def open_shell_with_command(command_string):
    # Start the command with pexpect
    command_string += """ --output-dir="commix_output" """
    proc = pexpect.spawn(command_string)

    # Start a separate thread to read the output from the process
    output_thread = threading.Thread(target=read_output, args=(proc,))
    output_thread.daemon = True
    output_thread.start()

    try:
        while True:
            # Read user input
            user_input = input("Enter command: ")

            # If the user types 'exit', break the loop and close the shell
            if user_input.strip().lower() == 'exit':
                proc.sendline('exit')
                break

            # Send the user input to the shell process
            proc.sendline(user_input)

    except KeyboardInterrupt:
        print("\nTerminating the shell.")
    finally:
        # Clean up: Close the process
        proc.close()
        output_thread.join()


class Commix(BaseModel):
    command: str = Field(description="""This tool has the same options and arguments as Commix command line tool.""")


@tool("commix",args_schema=Commix)
def commix(command: str):
    """This tool is an implementation of Commix"""
    print(f"this is the command: {command}")
    open_shell_with_command(command) 
    return command


# tools = load_tools(["terminal"], llm=llm, allow_dangerous_tools=True)
tools = [commix]
base_prompt = hub.pull("langchain-ai/react-agent-template")

instructions = sys.argv[1]

prompt = base_prompt.partial(instructions=instructions)
agent = create_react_agent(llm,tools,prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

print(f"Welcome to my application.  I am configured with these tools")
for tool in tools:
  print(f'  Tool: {tool.name} = {tool.description}')

while True:
    try:
        line = input("llm>> ")
        if line:
            result = agent_executor.invoke({"input":line})
            print(result)
        else:
            break
    except Exception as e:
        print(e)
