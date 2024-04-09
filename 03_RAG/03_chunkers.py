from langchain_google_genai import GoogleGenerativeAI
from langchain_community.document_loaders import AsyncHtmlLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import importlib
import time

module = importlib.import_module("01_loaders_transformers")
llm = GoogleGenerativeAI(model="gemini-pro")

loader = AsyncHtmlLoader("https://pdx.edu/computer-science")
docs = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size = 10000, chunk_overlap=1000)
docs_splits = text_splitter.split_documents(docs)
print(f"Split {len(docs[0].page_content)} byte document into {len(docs_splits)}")

article_chunks = [i for i in range(len(docs_splits)) if '<article>' in docs_splits[i].page_content]

for i in article_chunks:
    print(f"Found chunk {i} with <article> tag.  Sending to LLM")
    module.query_page(docs_splits[i].page_content)
