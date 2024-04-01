from langchain_google_genai import GoogleGenerativeAI
from langchain_core.messages import (
    HumanMessage,
    SystemMessage,
)
import readline

def spam_detector(llm, message):
    result = llm.invoke([
        SystemMessage(content="""You are a helpful spam detector.  Summarize the message given by the human and determine if it is malicious or benign"""),
        HumanMessage(content=message),
        ]
    )
    return(result)

llm = GoogleGenerativeAI(model="gemini-pro")

while True:
    line = input("llm>> ")
    if line:
        result = llm.invoke(spam_detector(llm,line))
        print(result)
    else:
        break
