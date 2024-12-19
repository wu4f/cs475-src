from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
from langchain.prompts import MessagesPlaceholder, HumanMessagePromptTemplate, ChatPromptTemplate
from langchain.memory import ConversationBufferMemory
import readline

llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest",temperature=0)

memory = ConversationBufferMemory(memory_key="messages", return_messages=True)

prompt = ChatPromptTemplate(
    input_variables=["content", "messages"],
    messages=[
        MessagesPlaceholder(variable_name="messages"),
        HumanMessagePromptTemplate.from_template("{content}")
    ]
)

chain = LLMChain(llm=llm, prompt=prompt, memory=memory, verbose=True)

print("Welcome to my chat application.  A blank line exits.")
while True:
    content = input(">> ")
    if content:
        result = chain.invoke({"content": content})
        print(result["text"])
    else:
        break
    #print(f"Current chat messages: {memory}")
