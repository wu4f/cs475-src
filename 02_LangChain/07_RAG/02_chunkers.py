import os
import importlib
from langchain_community.document_loaders import AsyncHtmlLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI
llm = ChatGoogleGenerativeAI(model=os.getenv("GOOGLE_MODEL"),temperature=0)
#from langchain_openai import ChatOpenAI
#llm = ChatOpenAI(model=os.getenv("OPENAI_MODEL"))
#from langchain_anthropic import ChatAnthropic
#llm = ChatAnthropic(model=os.getenv("ANTHROPIC_MODEL"))

module = importlib.import_module("01_loaders_transformers")

loader = AsyncHtmlLoader("https://www.pdx.edu/academics/programs/undergraduate/computer-science")
docs = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size = 5000, chunk_overlap=1000)
docs_splits = text_splitter.split_documents(docs)
print(f"Split {len(docs[0].page_content)} byte document into {len(docs_splits)}")

article_chunks = [i for i in range(len(docs_splits)) if 'job placement' in docs_splits[i].page_content]

for i in article_chunks:
    print(f"Found chunk {i} with 'job placement' in it.  Sending to LLM")
    module.query_page(docs_splits[i].page_content)
