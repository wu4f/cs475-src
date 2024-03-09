from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="gemini-pro-vision")

def query(llm, query, image_url):
  input(f"Q: {query} {image_url}")
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

image_url = 'https://portswigger.net/cms/images/91/43/e4e5-article-popovers-hidden-inputs.png'

print(query(llm, "What is going on in this image?", image_url))
