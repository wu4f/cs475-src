from langchain import hub
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_google_genai import GoogleGenerativeAI, GoogleGenerativeAIEmbeddings
import readline

vectorstore = Chroma(
     persist_directory="./rag_data/.chromadb",
     embedding_function=GoogleGenerativeAIEmbeddings(model="models/embedding-001", task_type="retrieval_query")
)

retriever = vectorstore.as_retriever()

prompt = hub.pull("rlm/rag-prompt")
print(f"prompt is: {prompt}")

llm = GoogleGenerativeAI(model="gemini-pro")

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

while True:
    line = input("llm>> ")
    if line:
        print(rag_chain.invoke(line))
    else:
        break
