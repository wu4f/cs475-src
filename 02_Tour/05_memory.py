import os
from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder
)
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_google_genai import ChatGoogleGenerativeAI

# Set up the LLM
llm = ChatGoogleGenerativeAI(model=os.getenv("GOOGLE_MODEL"))

# Create the prompt
prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template("You are a helpful assistant for the Generative Security class at Portland State University."),
    MessagesPlaceholder(variable_name="history"),
    HumanMessagePromptTemplate.from_template("{input}")
])

# Create the chain
chain = prompt | llm

# Session ID (can be dynamic per user/session)
session_id = "psu-gensec-session"

# Store the history instance separately so we can print it
message_history = InMemoryChatMessageHistory()

# Wrap with memory mechanism
chat_chain = RunnableWithMessageHistory(
    chain,
    lambda session_id: message_history,  # You could also return a new one per session
    input_messages_key="input",
    history_messages_key="history"
)

# Helper to print the message history
def pretty_print_history(messages):
    print("  History")
    print("  =======")
    for i, msg in enumerate(messages, start=1):
        role = "User" if msg.type == "human" else ("Assistant" if msg.type == "ai" else "System")
        print(f"  {i}. {role}: {msg.content}")
    print("  =======")

# Interactive chat loop
print("Welcome to the Generative Security chat application. A blank line exits.")
while True:
    content = input(">> ")
    if content:
        response = chat_chain.invoke({"input": content}, config={"configurable": {"session_id": session_id}})
        print(response.content)

        # Print the history from the retained instance
        pretty_print_history(message_history.messages)
    else:
        break

