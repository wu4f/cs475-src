import os
from langchain_google_genai import ChatGoogleGenerativeAI
llm = ChatGoogleGenerativeAI(model=os.getenv("GOOGLE_MODEL"),temperature=0)
response = llm.invoke("Write me a haiku about Portland State University")
print(response)

from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model=os.getenv("OPENAI_MODEL"))
response = llm.invoke("Write me a haiku about Portland State University")
print(response)

from langchain_anthropic import ChatAnthropic
llm = ChatAnthropic(model=os.getenv("ANTHROPIC_MODEL"))
response = llm.invoke("Write me a haiku about Portland State University")
print(response)

from langchain_xai import ChatXAI
llm = ChatXAI(model=os.getenv("XAI_MODEL"))
response = llm.invoke("Write me a haiku about Portland State University")
print(response)
