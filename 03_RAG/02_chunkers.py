from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
import requests
import argparse
import os

from .print_helpers import *

def langchain_loader_comparison(path):
    """
    Compare document loading methods.

    This function tries to load pdf with traditional LangChain PyPDFLoader

    Args:
        path (str): The path to the PDF files.

    Returns:
        None
    """
    print(f"Loading PDF files from: {path}")
    loader = PyPDFLoader(path)
    docs = loader.load()
    print(docs)

def recursive_chunker():
    """
    Chunk text recursively.

    This function demonstrates the recursive chunking of text.

    Args:
        None

    Returns:
        None
    """
    text = """ One of the most important things I didn't understand about the world when I was a child is the degree to which the returns for performance are superlinear. Teachers and coaches implicitly told us the returns were linear. "You get out," I heard a thousand times, "what you put in." They meant well, but this is rarely true. If your product is only half as good as your competitor's, you don't get half as many customers. You get no customers, and you go out of business. It's obviously true that the returns for performance are superlinear in business. Some think this is a flaw of capitalism, and that if we changed the rules it would stop being true. But superlinear returns for performance are a feature of the world, not an artifact of rules we've invented. We see the same pattern in fame, power, military victories, knowledge, and even benefit to humanity. In all of these, the rich get richer. [1] """

    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 65, chunk_overlap=0)

    docs = text_splitter.create_documents([text])

    text = [chunk.page_content for chunk in docs ]

    print_chunks(text)

    
def unstructured_chunked_pdf(pdf_path):
    """
    Extract and chunk text from an unstructured PDF.

    This function extracts text from an PDF, chunks it using Unstructured API, and prints the chunks.

    Args:
        pdf_path (str): The path to the unstructured PDF.

    Returns:
        None
    """
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
    data = {"strategy": "hi_res" ,
            "chunking_strategy": "by_title",
            "max_characters": MAX_CHARACTERS, 
            "combine_text_under_n_chars": COMBINE_UNDER_N_CHARS, 
            "overlap": 100}
    files = {"files": open(pdf_path, "rb")}
    response = requests.post(UNSTRUCTURED_URL, headers=headers, files=files, data=data)
    if response.status_code == 200:
        # process response.json()
        result = response.json()
        result = [res["text"] for res in result]
        print_chunks(result)
    else:
        print("Error processing request. Check that the endpoint is correct. Also double check your API key. If it still doesn't work it is possibel that the API key and endpoint is still be activated. Return to exerise later.")

def chunker_example():
    """
    Example of document chunking.

    This function provides an example of document chunking using both LangChain PDFLoader and Unstructured PDF loader/extractor.

    Args:
        None

    Returns:
        None
    """
    pdf_path = "./rag_data/pdf/msSecurity-compressed-extracted.pdf"
    print_with_hashtag("LangChain PDFLoader output")
    langchain_loader_comparison(pdf_path)
    print_with_hashtag("Unstructured pdf loader/extractor")
    unstructured_chunked_pdf(pdf_path)

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
    parser.add_argument("-f", "--function", type=str, choices=["recursive_chunker","document_chunker"], help="Choose function to execute (summarizer,recursive_url)")

    # Parse the command line arguments
    args = parser.parse_args()

    # Determine which function to call based on the command line argument
    if args.function == "recursive_chunker":
        recursive_chunker()
    elif args.function == "document_chunker":
        chunker_example()
    else:
        print("Please enter function choice (recursive_chunker, document_chunker) as an argument to the option -f.")
        print("Example: python 03_document_loaders.py -f summarizer")

if __name__ == "__main__":
    # article_summarizer_no_chunking()
    # useful_document_loaders()
    main_driver()