from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
import readline

llm = ChatGoogleGenerativeAI(model="gemini-pro-vision")

def query_llm(llm, query, image_url):
  message = HumanMessage(
      content=[
          {
              "type": "text",
              "text": query,
          },
          {   "type": "image_url",
              "image_url": image_url
          }
      ]
  )
  response = llm.invoke([message])
  return response

prompt = "What is going on in this image?"
image_url = 'https://portswigger.net/cms/images/91/43/e4e5-article-popovers-hidden-inputs.png'

print("This application tells you what's going on with an image given its URL.  Enter a URL: ")
while True:
    line = input("llm>> ")
    if line:
       print(query_llm(llm, prompt, line))
    else:
       break
