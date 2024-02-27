from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import GoogleGenerativeAI

llm = GoogleGenerativeAI(model="gemini-pro")

prompt = ChatPromptTemplate.from_template("Tell me a joke about {topic}")
output_parser = StrOutputParser()

chain = (
    {"topic": RunnablePassthrough()} 
    | prompt
    | llm
    | output_parser
)

print("Welcome to my joke application.  Type a topic and I will tell you a joke about it.")
while True:
    try:
        line = input("llm>> ")
        if line:
            result = chain.invoke(line)
            print(result)
        else:
            break
    except:
        break
