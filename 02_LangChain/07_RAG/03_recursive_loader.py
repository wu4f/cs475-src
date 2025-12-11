from langchain_community.document_loaders.recursive_url_loader import RecursiveUrlLoader
from bs4 import BeautifulSoup
import re

def get_body(page):
   new_page = re.sub('<br />','  ', page)
   body = BeautifulSoup(new_page, "html.parser").find('body')
   if body:
       return(re.sub('\n',' ', body.get_text()))

loader = RecursiveUrlLoader(
             url = "https://web.cs.pdx.edu",
             max_depth = 2,
             extractor=lambda x: get_body(x)
)

docs = loader.load()
print(f"Downloaded and parsed {len(docs)} URLs")
