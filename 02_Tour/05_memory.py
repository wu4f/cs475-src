from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory
import readline
from langchain.prompts import (
    ChatPromptTemplate, 
    SystemMessagePromptTemplate, 
    HumanMessagePromptTemplate, 
    MessagesPlaceholder
)

def pretty_print_history(messages):
    print("  History")
    print("  =======")
    for i, msg in enumerate(messages, start=1):
        role = "User" if msg.type == "human" else ("Assistant" if msg.type == "ai" else "System")
        print(f"  {i}. {role}: {msg.content}")
    print("  =======")

llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest",temperature=0)

memory = ConversationBufferMemory(return_messages=True)

prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template("You are a helpful assistant for the Generative Security class at Portland State University."),
    MessagesPlaceholder(variable_name="history"),
    HumanMessagePromptTemplate.from_template("{input}")
])

chain = prompt | llm

print("Welcome to the Generative Security chat application.  A blank line exits.")
while True:
    content = input(">> ")
    if content:
        memory_vars = memory.load_memory_variables({})
        response = chain.invoke({"history": memory_vars["history"], "input": content})
        result = response.content
        print(result)
        memory.save_context({"input": content}, {"output": result})
        pretty_print_history(memory_vars['history'])
    else:
        break

