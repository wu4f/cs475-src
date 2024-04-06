from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import AsyncHtmlLoader, DirectoryLoader, TextLoader, PyPDFDirectoryLoader, Docx2txtLoader, UnstructuredMarkdownLoader
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

vectorstore = Chroma(
    embedding_function=GoogleGenerativeAIEmbeddings(model="models/embedding-001", task_type="retrieval_query"),
    persist_directory="./rag_data/.chromadb"
)

def load_urls(vectorstore, urls):
    print(f"Loading: {urls}")
    loader = AsyncHtmlLoader(urls)
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    vectorstore.add_documents(documents=splits)

def load_pdf(vectorstore, directory):
    print(f"Loading PDF files from: {directory}")
    loader = PyPDFDirectoryLoader(directory)
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=10)
    splits = text_splitter.split_documents(docs)
    vectorstore.add_documents(documents=splits)

def load_txt(vectorstore, directory):
    print(f"Loading TXT files from: {directory}")
    loader = DirectoryLoader(directory, glob="**/*.txt", loader_cls=TextLoader)
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=10)
    splits = text_splitter.split_documents(docs)
    vectorstore.add_documents(documents=splits)

def load_docx(vectorstore, directory):
    print(f"Loading DOCX files from: {directory}")
    loader = DirectoryLoader(directory, glob="**/*.docx", loader_cls=Docx2txtLoader)
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=10)
    splits = text_splitter.split_documents(docs)
    vectorstore.add_documents(documents=splits)

def load_md(vectorstore, directory):
    print(f"Loading MD files from: {directory}")
    loader = DirectoryLoader(directory, glob="**/*.md", loader_cls=UnstructuredMarkdownLoader)
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=10)
    splits = text_splitter.split_documents(docs)
    vectorstore.add_documents(documents=splits)

def search_db(vectorstore, query):
    docs = vectorstore.similarity_search(query)
    print(f"Query database for: {query}")
    if docs:
        print(f"Closest document match in database: {docs[0].metadata}")
    else:
        print("No matching documents")

load_urls(vectorstore, ["https://en.wikipedia.org/wiki/LangChain","https://api.python.langchain.com/en/latest/langchain_api_reference.html","https://en.wikipedia.org/wiki/President_of_the_United_States"])
load_pdf(vectorstore, "rag_data/pdf")
load_txt(vectorstore, "rag_data/txt")
load_docx(vectorstore, "rag_data/docx")
load_md(vectorstore, "rag_data/md")
search_db(vectorstore, "Who is the President of the United States?")
search_db(vectorstore, "What are data types in Python?")
search_db(vectorstore, "What is the first ammendment of the Constitution?")
search_db(vectorstore, "What are some famous quotes from Martin Luther King Jr?")
search_db(vectorstore, "How do you create a heading in Markdown?")
