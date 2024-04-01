from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import GoogleGenerativeAI
import readline

llm = GoogleGenerativeAI(model="gemini-pro")

prompt1 = PromptTemplate.from_template("Translate this text to Spanish and print both the original and the translation: {text}")
prompt2 = PromptTemplate.from_template("Write another phrase that might follow the {translation} in Spanish and output both the translation and the additional phrase")
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

print("Welcome to my multi-lingual conversation completer.  Type an English phrase and I will translate it to Spanish and then generate another phrase that might follow it.")

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
