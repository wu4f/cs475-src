from langchain_community.document_loaders.recursive_url_loader import RecursiveUrlLoader
from bs4 import BeautifulSoup
import re

def get_article(page):
   new_page = re.sub('<br />','  ', page)
   article = BeautifulSoup(new_page, "html.parser").find('article')
   if article:
       return(re.sub('\n',' ',article.get_text()))

loader = RecursiveUrlLoader(
             url = "https://pdx.edu/computer-science",
             max_depth = 2,
             extractor=lambda x: get_article(x)
)

docs = loader.load()
print(f"Downloaded and parsed {len(docs)} URLs")
