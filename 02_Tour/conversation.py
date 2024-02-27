# Requires export GOOGLE_API_KEY=""
from langchain_core.messages import HumanMessage
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

while True:
    content = input(">> ")
    result = chain.invoke({"content": content})
    print(result["text"])
    print(f"Current chat messages: {memory}")
