from langchain_google_genai import GoogleGenerativeAI
llm = GoogleGenerativeAI(model="gemini-pro")
response = llm.invoke("Write me a haiku about Portland State University")
print(response)
