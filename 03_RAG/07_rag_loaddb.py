from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import AsyncHtmlLoader, DirectoryLoader, TextLoader, PyPDFDirectoryLoader, Docx2txtLoader, UnstructuredMarkdownLoader, WikipediaLoader, ArxivLoader, CSVLoader
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

def load_txt(directory):
    load_docs(DirectoryLoader(directory, glob="**/*.txt", loader_cls=TextLoader).load())

def load_pdf(directory):
    load_docs(PyPDFDirectoryLoader(directory).load())

def load_docx(directory):
    load_docs(DirectoryLoader(directory, glob="**/*.docx", loader_cls=Docx2txtLoader).load())

def load_md(directory):
    load_docs(DirectoryLoader(directory, glob="**/*.md", loader_cls=UnstructuredMarkdownLoader).load())

def load_csv(directory):
    load_docs(DirectoryLoader(directory, glob="**/*.csv", loader_cls=CSVLoader).load())

urls = ["https://www.pdx.edu/academics/programs/undergraduate/computer-science", "https://www.pdx.edu/computer-science/"]
print(f"Loading: {urls}")
load_urls(urls)

wiki_query = "LangChain"
print(f"Loading Wikipedia pages on: {wiki_query}")
load_wikipedia(wiki_query)

arxiv_query = "2310.03714"
print(f"Loading arxiv document: {arxiv_query}")
load_arxiv(arxiv_query)

text_directory = "rag_data/txt"
print(f"Loading TXT files from: {text_directory}")
load_txt(text_directory)

pdf_directory = "rag_data/pdf"
print(f"Loading PDF files from: {pdf_directory}")
load_pdf(pdf_directory)

docx_directory = "rag_data/docx"
print(f"Loading DOCX files from: {docx_directory}")
load_docx(docx_directory)

md_directory = "rag_data/md"
print(f"Loading MD files from: {md_directory}")
load_md(md_directory)

csv_directory = "rag_data/csv"
print(f"Loading CSV files from: {csv_directory}")
load_csv(csv_directory)

print("RAG database initialized with the following sources.")
retriever = vectorstore.as_retriever()
document_data_sources = set()
for doc_metadata in retriever.vectorstore.get()['metadatas']:
    document_data_sources.add(doc_metadata['source']) 
for doc in document_data_sources:
    print(f"  {doc}")
