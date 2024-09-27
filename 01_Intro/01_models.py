from langchain_google_genai import ChatGoogleGenerativeAI
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro")
response = llm.invoke("Write me a haiku about Portland State University")
print(response)

from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4o")
response = llm.invoke("Write me a haiku about Portland State University")
print(response)

from langchain_anthropic import ChatAnthropic
llm = ChatAnthropic(model="claude-3-opus-20240229")
response = llm.invoke("Write me a haiku about Portland State University")
print(response)
