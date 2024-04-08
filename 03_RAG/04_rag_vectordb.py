from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import AsyncHtmlLoader, DirectoryLoader, TextLoader, PyPDFDirectoryLoader, Docx2txtLoader, UnstructuredMarkdownLoader, WikipediaLoader, ArxivLoader
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import readline

vectorstore = Chroma(
    embedding_function=GoogleGenerativeAIEmbeddings(model="models/embedding-001", task_type="retrieval_query"),
    persist_directory="./rag_data/.chromadb"
)

def load_docs(docs):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=10)
    splits = text_splitter.split_documents(docs)
    vectorstore.add_documents(documents=splits)

def load_urls(urls):
    load_docs(AsyncHtmlLoader(urls).load())

def load_wikipedia(query):
    load_docs(WikipediaLoader(query=query, load_max_docs=1).load())

def load_arxiv(query):
    docs = ArxivLoader(query=query, load_max_docs=1).load()
    docs[0].metadata['source'] = f"arxiv:{query}"
    load_docs(docs)

def load_pdf(directory):
    load_docs(PyPDFDirectoryLoader(directory).load())

def load_txt(directory):
    load_docs(DirectoryLoader(directory, glob="**/*.txt", loader_cls=TextLoader).load())

def load_docx(directory):
    load_docs(DirectoryLoader(directory, glob="**/*.docx", loader_cls=Docx2txtLoader).load())

def load_md(directory):
    load_docs(DirectoryLoader(directory, glob="**/*.md", loader_cls=UnstructuredMarkdownLoader).load())

def search_db(query):
    docs = vectorstore.similarity_search(query)
    print(f"Query database for: {query}")
    if docs:
        print(f"Closest document match in database: {docs[0].metadata['source']}")
        #print(f"Closest document match in database: {docs[0].metadata}")
    else:
        print("No matching documents")

print(f"Loading: {urls}")
load_urls(["https://www.pdx.edu/", "https://www.pdx.edu/computer-science/"])
print(f"Loading Wikipedia pages on: {query}")
load_wikipedia("LangChain")
print(f"Loading arxiv document: {query}")
load_arxiv("2310.03714")
print(f"Loading PDF files from: {directory}")
load_pdf("rag_data/pdf")
print(f"Loading TXT files from: {directory}")
load_txt("rag_data/txt")
print(f"Loading DOCX files from: {directory}")
load_docx("rag_data/docx")
print(f"Loading MD files from: {directory}")
load_md("rag_data/md")

print("RAG database initialized.")
retriever = vectorstore.as_retriever()
document_data_sources = set()
for doc_metadata in retriever.vectorstore.get()['metadatas']:
    document_data_sources.add(doc_metadata['source']) 
for doc in document_data_sources:
    print(f"  {doc}")

while True:
    line = input("llm>> ")
    if line:
        search_db(line)
    else:
        break
