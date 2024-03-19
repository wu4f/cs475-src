from langchain_google_genai import GoogleGenerativeAI
from langchain_core.messages import (
    HumanMessage,
    SystemMessage,
)

def spam_detector(llm, message):
    result = llm.invoke([
        SystemMessage(content="You are a helpful spam detector.  Do your best to classify the message given by the human as malicious or benign"),
        HumanMessage(content=f"{message}"),
        ]
    )
    return(result)

llm = GoogleGenerativeAI(model="gemini-pro")

message = "Win $1000.  Click on this attachment to find out how! Offer ends in 1 hour"
print(spam_detector(llm,message))

message = "This is to notify you that the e-mail contact information for your account was just changed.  If you did not request this change, please contact customer service at the number listed on your account statement."
print(spam_detector(llm,message))
