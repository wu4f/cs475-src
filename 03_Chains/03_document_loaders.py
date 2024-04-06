#Import Modules
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders.recursive_url_loader import RecursiveUrlLoader
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.document_loaders import ArxivLoader
from langchain_community.document_loaders import WikipediaLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFDirectoryLoader

from langchain_community.document_loaders import PyPDFLoader
from langchain.chains import StuffDocumentsChain
from langchain.chains.llm import LLMChain
from bs4 import BeautifulSoup as Soup
from langchain.prompts import PromptTemplate
import requests
import argparse
import os
from pypdf import PdfReader

#Initialize Model
llm = ChatGoogleGenerativeAI(model="gemini-pro")

#Basic data processing using WebBaseLoader
def article_summarizer_no_chunking():
    loader = WebBaseLoader("https://thenewstack.io/the-building-blocks-of-llms-vectors-tokens-and-embeddings/")
    docs = loader.load()

    #Define the Summarize Chain
    template = """Write a concise summary of the following:
    "{text}"
    CONCISE SUMMARY:"""

    prompt = PromptTemplate.from_template(template)

    llm_chain = LLMChain(llm=llm, prompt=prompt)
    stuff_chain = StuffDocumentsChain(llm_chain=llm_chain, document_variable_name="text")

    #Invoke Chain
    response=stuff_chain.invoke(docs)
    print(response["output_text"])
    print('---------------------------------------------------')

def recursive_loader(url):
    loader = RecursiveUrlLoader(
        url=url, max_depth=2, exclude_dirs=["/_static"] , extractor=lambda x: Soup(x, "html.parser").text
    )
    docs = loader.load()
    for i in docs:
        if ".xml" in i.metadata["source"]:
            print(i.metadata)
        else: 
            print(i.metadata["source"])

def recursive_loader():
    recursive_loader_url = "https://docs.python.org/3.9/"
    recursive_loader(recursive_loader_url)


def csv_loader():
    loader = CSVLoader("./chunk_data/csv/gemini_generated.csv")
    docs = loader.load()
    for i in docs:
        print(i)

def arxiv_loader():
    loader = ArxivLoader(query="2310.03714", load_max_docs=2)
    docs = loader.load()
    len(docs)

    print(docs[0].metadata)
    print(docs[0].page_content[:200])

def wikipedia_loader():
    loader = WikipediaLoader(query="LLM Pipelines", load_max_docs=2)
    docs = loader.load()
    len(docs)

    print(docs[0].metadata)
    print(docs[0].page_content[:200])

    print(docs[1].metadata)
    print(docs[1].page_content[:200])


def print_with_hashtag(string):
    length = len(string)
    print("#" * (length + 4))
    print("# " + string + " #")
    print("#" * (length + 4))


def print_chunks(chunkers):
    for i, chunk in enumerate(chunkers):
        print_with_hashtag(f"Chunk {i}")
        print(chunk)
        print("\n\n" + "-"*80)

def langchain_loader_comparison(path):
    print(f"Loading PDF files from: {path}")
    loader = PyPDFLoader(path)
    docs = loader.load()
    print(docs)

def recursive_chunker():
    text = """ One of the most important things I didn't understand about the world when I was a child is the degree to which the returns for performance are superlinear. Teachers and coaches implicitly told us the returns were linear. "You get out," I heard a thousand times, "what you put in." They meant well, but this is rarely true. If your product is only half as good as your competitor's, you don't get half as many customers. You get no customers, and you go out of business. It's obviously true that the returns for performance are superlinear in business. Some think this is a flaw of capitalism, and that if we changed the rules it would stop being true. But superlinear returns for performance are a feature of the world, not an artifact of rules we've invented. We see the same pattern in fame, power, military victories, knowledge, and even benefit to humanity. In all of these, the rich get richer. [1] """

    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 65, chunk_overlap=0)

    docs = text_splitter.create_documents([text])

    text = [chunk.page_content for chunk in docs ]

    print_chunks(text)




    
def unstructured_chunked_pdf(pdf_path):
    UNSTRUCTURED_API_KEY = os.environ.get('UNSTRUCTURED_API_KEY')
    if UNSTRUCTURED_API_KEY is None:
        print("UNSTRUCTURED_API_KEY environment variable not set.")
        return
    UNSTRUCTURED_URL = os.environ.get('UNSTRUCTURED_URL')
    if UNSTRUCTURED_URL is None:
        print("UNSTRUCTURED_URL environment variable not set.")
        return

    headers = {'accept': 'application/json', 'unstructured-api-key': UNSTRUCTURED_API_KEY }
    MAX_CHARACTERS = 500
    COMBINE_UNDER_N_CHARS = 2000
    strategy = {"strategy":"hi_res"}
    response = requests.post(UNSTRUCTURED_URL, headers=headers, files={"files": open(pdf_path, "rb")}, data={"strategy": "hi_res" ,"chunking_strategy": "by_title","max_characters": MAX_CHARACTERS, "combine_text_under_n_chars": COMBINE_UNDER_N_CHARS, "overlap": 100})
    if response.status_code == 200:
        # process response.json()
        result = response.json()
        result = [res["text"] for res in result]
        print_chunks(result)
    else:
        print("Error processing request. Check that the endpoint is correct. Also double check your API key. If it still doesn't work it is possibel that the API key and endpoint is still be activated. Return to exerise later.")

def chunker_example():
    pdf_path = "./chunk_data/pdf/msSecurity-compressed-extracted.pdf"
    print_with_hashtag("LangChain PDFLoader output")
    langchain_loader_comparison(pdf_path)
    print_with_hashtag("Unstructured pdf loader/extractor")
    unstructured_chunked_pdf(pdf_path)



def other_loaders():
    print("\n")
    print("arXiv example")
    print("----------------------------------------")
    arxiv_loader() 
    print("\n\n\n\n\n")
    print("Wikipedia example")
    print("----------------------------------------")
    wikipedia_loader()


def main_driver():
    # Create argument parser
    parser = argparse.ArgumentParser(description="Show the ELT data pipeline with langchain loaders, chunkers, and tokenizers")

    # Add arguments for each function
    parser.add_argument("-f", "--function", type=str, choices=["summarizer", "recursive_url", "other_loaders", "recursive_chunker","document_chunker", "tokenizers"], help="Choose function to execute (summarizer,recursive_url,other_loaders, recursive_chunker, document_chunker, tokenizer)")

    # Parse the command line arguments
    args = parser.parse_args()

    # Determine which function to call based on the command line argument
    if args.function == "summarizer":
        article_summarizer_no_chunking()
    elif args.function == "recursive_url":
        recursive_loader()
    elif args.function == "csv_loader":
        csv_loader()
    elif args.function == "other_loaders":
        other_loaders()
    elif args.function == "recursive_chunker":
        recursive_chunker()
    elif args.function == "document_chunker":
        chunker_example()
    elif args.function == "tokenizers":
        print("Function 5 called")

    else:
        print("Please enter function choice (summarizer, recursive_loader, recursive_chunker, document_chunker, tokenizer) as an argument to the option -f.")
        print("Example: python 03_document_loaders.py -f summarizer")

if __name__ == "__main__":
    # article_summarizer_no_chunking()
    # useful_document_loaders()
    main_driver()
