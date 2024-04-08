from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.document_loaders import AsyncHtmlLoader
from langchain_community.document_loaders.recursive_url_loader import RecursiveUrlLoader
from langchain.chains import StuffDocumentsChain
from langchain.chains.llm import LLMChain

from bs4 import BeautifulSoup as Soup
from langchain.prompts import PromptTemplate
import argparse

from .print_helpers import *

#Initialize Model
llm = ChatGoogleGenerativeAI(model="gemini-pro")

def article_summarizer_no_chunking():
    """
    Summarizes an article without chunking using WebBaseLoader.

    This function retrieves an article from a specified URL using WebBaseLoader, then generates a concise summary of the article content.
    It utilizes a language model chain to generate the summary.

    Args:
        None

    Returns:
        None
    """
    loader = AsyncHtmlLoader("https://thenewstack.io/the-building-blocks-of-llms-vectors-tokens-and-embeddings/")
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
    print(f"Title: {docs[0].metadata['title']}")
    print(f"Summary: {response['output_text']}")
    print('---------------------------------------------------')

def recursive_loader(url):
    """
    Load documents recursively from a specified URL.

    This function loads documents recursively from a given URL up to a maximum depth of 2.
    It excludes specific directories and utilizes BeautifulSoup for parsing HTML content.

    Args:
        url (str): The URL from which to load documents recursively.

    Returns:
        None
    """
    loader = RecursiveUrlLoader(
        url=url, max_depth=2, exclude_dirs=["/_static"] , extractor=lambda x: Soup(x, "html.parser").text
    )
    docs = loader.load()
    print_with_hashtag("Scraped Documents")
    for i in docs:
        if ".xml" in i.metadata["source"]:
            print(i.metadata)
        else: 
            print(i.metadata["source"])

def main_driver():
    """
    Main driver function.

    This function parses command-line arguments and executes corresponding functions based on the provided arguments.

    Args:
        None

    Returns:
        None
    """
    # Create argument parser
    parser = argparse.ArgumentParser(description="Show the start of the ELT pipeline using LangChain Loaders.")

    # Add arguments for each function
    parser.add_argument("-f", "--function", type=str, choices=["summarizer", "recursive_url"], help="Choose function to execute (summarizer,recursive_url)")

    # Parse the command line arguments
    args = parser.parse_args()

    # Determine which function to call based on the command line argument
    if args.function == "summarizer":
        article_summarizer_no_chunking()
    elif args.function == "recursive_url":
        url = "https://docs.python.org/3.9/"
        recursive_loader(url)
    else:
        print("Please enter function choice (summarizer, recursive_loader) as an argument to the option -f.")
        print("Example: python 03_document_loaders.py -f summarizer")

if __name__ == "__main__":
    # article_summarizer_no_chunking()
    # useful_document_loaders()
    main_driver()

