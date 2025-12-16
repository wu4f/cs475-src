import os
import time
from langchain_community.document_loaders import AsyncHtmlLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
from langchain_google_genai import ChatGoogleGenerativeAI
llm = ChatGoogleGenerativeAI(model=os.getenv("GOOGLE_MODEL"),temperature=0)
#from langchain_openai import ChatOpenAI
#llm = ChatOpenAI(model=os.getenv("OPENAI_MODEL"))
#from langchain_anthropic import ChatAnthropic
#llm = ChatAnthropic(model=os.getenv("ANTHROPIC_MODEL"))

def query_page(content):
   print(f"Content size: {len(content)}")
   print(f"Content [:100]: {content[0:100]}")
   prompt = f"What percentage of graduates get jobs?  Answer based on the provided context. \n Context: {content}"
   start = time.time()
   response = llm.invoke(prompt)
   end = time.time()
   print(f"Time elapsed: {end-start} seconds\nResponse: {response}")

if __name__ == "__main__":
    loader = AsyncHtmlLoader(["https://www.pdx.edu/academics/programs/undergraduate/computer-science", ])
    docs = loader.load()
    print("========")
    print("Raw HTML")
    print("========")
    try:
        query_page(docs[0].page_content)
    except Exception as e:
        print(f"Error in query: {e}")
    print("===========")
    print("Parsed HTML")
    print("===========")
    bs_tr = BeautifulSoupTransformer()
    docs_tr = bs_tr.transform_documents(docs, tags_to_extract=["article"])
    try:
        query_page(docs_tr[0].page_content)
    except Exception as e:
        print(f"Error in query: {e}")
