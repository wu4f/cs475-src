from langchain_google_genai import ChatGoogleGenerativeAI
chat = ChatGoogleGenerativeAI(model="gemini-pro")
response = chat.invoke("Write me a haiku about Portland State University")
print(response.content)
