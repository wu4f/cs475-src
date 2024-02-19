from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAI
import chromadb
import os
from dotenv import load_dotenv

load_dotenv()

# Define embedding function
embedding_function = SentenceTransformerEmbeddings(model_name="all-mpnet-base-v2")

# Open vector database
current_directory = os.path.dirname("__file__")
chroma_db = os.path.join(current_directory, "./chroma_db")

persistent_client = chromadb.PersistentClient(path=chroma_db)
db = Chroma(
    client=persistent_client,
    collection_name="groups_collection",
    embedding_function=embedding_function,
)
db.get()
retriever = db.as_retriever(search_kwargs={"k":5})

# Instantiate LLM and QA chain
from langchain.chains.question_answering import load_qa_chain
llm = GoogleGenerativeAI(model="gemini-pro")
chain = load_qa_chain(llm, chain_type="stuff")

# Perform query by retrieving context and invoking chain
query = """What threat actors sent phishing messages to their targets?"""
print(f"[+] Getting relevant documents for: {query}")
relevant_docs = retriever.get_relevant_documents(query)
results = chain.invoke({'input_documents':relevant_docs, 'question':query})
print(f"[+] Output from chain is: {results['output_text']}")

query = """What threat actors sent messages to their targets over social media accounts?"""
print(f"[+] Getting relevant documents for: {query}")
relevant_docs = retriever.get_relevant_documents(query)
results = chain.invoke({'input_documents':relevant_docs, 'question':query})
print(f"[+] Output from chain is: {results['output_text']}")

query = "What are some phishing techniques used by threat actors?"
print(f"[+] Getting relevant documents for: {query}")
relevant_docs = retriever.get_relevant_documents(query)
results = chain.invoke({'input_documents':relevant_docs, 'question':query})
print(f"[+] Output from chain is: {results['output_text']}")
