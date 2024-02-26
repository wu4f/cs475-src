# Requires export GOOGLE_API_KEY=""
from langchain_google_genai import GoogleGenerativeAI
llm = GoogleGenerativeAI(model="gemini-pro")
prompt = "How do I get to Peru from Portland?"
input(f"Run query: {prompt}")
response = llm.invoke(prompt)
print(response)
query = "How do I get to Peru from Portland? Think step-by-step."
input(f"Run query: {prompt}")
response = llm.invoke(prompt)
print(response)
