from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
import readline

llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro")

chat_template = ChatPromptTemplate.from_messages(
    [
        ('system', 'Classify the following e-mail snippet using one of two words: Malicious or Benign.'),
        ('human', 'Message: Unclaimed winning ticket.  View attachment for instructions to claim.'),
        ('ai',"Malicious"),
        ('human', 'Message: Thanks for your interest in Generative AI'),
        ('ai','Benign'),
        ('human', 'Message: {message}')
    ]
)

print("Welcome to my chat model spam detector.  Type an e-mail subject line and I will tell you if it is benign or malicious.  A blank line exits.")
while True:
    line = input("llm>> ")
    if line:
        prompt = chat_template.format_messages(message=line)
        print(f"Rendered prompt is: {prompt}")
        result = llm.invoke(prompt)
        print(f"Result is: {result.content}")
    else:
        break

