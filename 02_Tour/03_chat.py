from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
from langchain.prompts import MessagesPlaceholder, HumanMessagePromptTemplate, ChatPromptTemplate
from langchain.memory import ConversationBufferMemory

llm = ChatGoogleGenerativeAI(model="gemini-pro")

memory = ConversationBufferMemory(memory_key="messages", return_messages=True)

prompt = ChatPromptTemplate(
    input_variables=["content", "messages"],
    messages=[
        MessagesPlaceholder(variable_name="messages"),
        HumanMessagePromptTemplate.from_template("{content}")
    ]
)

chain = LLMChain(llm=llm, prompt=prompt, memory=memory)

print("Welcome to my chat application.")
while True:
    content = input(">> ")
    if content:
        result = chain.invoke({"content": content})
        print(result["text"])
    else:
        break

#    print(f"Current chat messages: {memory}")
