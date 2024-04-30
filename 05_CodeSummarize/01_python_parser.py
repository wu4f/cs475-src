from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import LanguageParser
from langchain_text_splitters import Language
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import readline
#llm = GoogleGenerativeAI(model="gemini-1.5-pro-latest",temperature=0)
llm = GoogleGenerativeAI(model="gemini-pro",temperature=0)

def summarize_file(file):
    loader = GenericLoader.from_filesystem(
            file,
            glob="*",
            suffixes=[".py"],
            parser=LanguageParser(),
    )
    docs = loader.load()
    prompt1 = PromptTemplate.from_template("Summarize this Python code: {text}")
    output_parser = StrOutputParser()

    chain = (
      {"text": RunnablePassthrough()} 
      | prompt1
      | llm
      | output_parser
    )
    output = "\n".join([d.page_content for d in docs])

    result = chain.invoke(output)
    return(result)

print("Welcome to my code summarizer.  Give me a path to a Python program and I'll summarize it.")

while True:
    try:
        line = input("llm>> ")
        if line:
            result = summarize_file(line)
            print(result)
        else:
            break
    except Error as e:
        print(e)
        break
