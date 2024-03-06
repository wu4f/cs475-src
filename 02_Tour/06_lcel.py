from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import GoogleGenerativeAI

llm = GoogleGenerativeAI(model="gemini-pro")

prompt1 = PromptTemplate.from_template("Translate this text to Spanish {text}")
prompt2 = PromptTemplate.from_template("Produce the ASCII hexadecimal encoding of the translation, putting spaces between each character encoding: {translation}")
output_parser = StrOutputParser()

chain = (
    {"text": RunnablePassthrough()} 
    | prompt1
    | llm
    | {"translation": RunnablePassthrough()} 
    | prompt2
    | llm
    | output_parser
)

print("Welcome to my application.  Type an English phrase and I will translate it to Spanish, and then back into English.")

while True:
    try:
        line = input("llm>> ")
        if line:
            result = chain.invoke({"text":line})
            print(result)
        else:
            break
    except:
        break
