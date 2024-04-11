from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import readline

vectorstore = Chroma(
    embedding_function=GoogleGenerativeAIEmbeddings(model="models/embedding-001", task_type="retrieval_query"),
    collection_name="groups_collection",
    persist_directory="./mitre_rag_data/.chromadb"
)

def search_db(query):
    print(f'[+] Test similarity search with query: {query}')
    relevant_docs = vectorstore.similarity_search(query)
    print(f"Search returned {len(relevant_docs)} documents")
    for doc in relevant_docs:
        print(doc.metadata['source'])
    #return(relevant_docs)

#print(f'[+] Results of retrieval for query: {query}')
#print(relevant_docs[0].page_content)


while True:
    line = input("llm>> ")
    if line:
        search_db(line)
    else:
        break
