from langchain_google_genai import GoogleGenerativeAI
llm = GoogleGenerativeAI(model="gemini-1.5-pro-latest",temperature=0)
response = llm.invoke("Write me a haiku about Portland State University")
print(response)
