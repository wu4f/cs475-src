#Import Modules
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders.recursive_url_loader import RecursiveUrlLoader
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.document_loaders import ArxivLoader

from langchain.chains import StuffDocumentsChain
from langchain.chains.llm import LLMChain
from bs4 import BeautifulSoup as Soup
from langchain.prompts import PromptTemplate
import argparse

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
#Chunking examples
def csv_loader():
    loader = CSVLoader("https://raw.githubusercontent.com/datasets/covid-19/main/data/countries-aggregated.csv")
    docs = loader.load()
    for i in docs:
        print(i.metadata)

def useful_document_loaders():


def main_driver():


    # Define your functions here
    def function1():
        print("Function 1 called")

    def function2():
        print("Function 2 called")

    def function3():
        print("Function 3 called")

    # Create argument parser
    parser = argparse.ArgumentParser(description="Description of your program")

    # Add arguments for each function
    parser.add_argument("-f", "--function", type=str, choices=["summarizer", "recursive_url", "other_loaders", "chunkers", "tokenizers"], help="Choose function to execute (summarizer,recursive_url,other_loaders, chunkers, tokenizer)")

    # Parse the command line arguments
    args = parser.parse_args()

    # Determine which function to call based on the command line argument
    if args.function == "summarizer":
        function1()
    elif args.function == "recursive_url":
        function2()
    elif args.function == "other_loaders":
        function3()
    elif args.function == "chunkers":
        print("Function 4 called")
    elif args.function == "tokenizers":
        print("Function 5 called")

    else:
        print("Please enter function choice (summarizer, recursive_loader, recursive_chunker, tokenizer, ) as an argument to the option -f.")
        print("Example: python 03_document_loaders.py -f summarizer")

if __name__ == "__main__":
    # article_summarizer_no_chunking()
    # useful_document_loaders()
    main_driver()