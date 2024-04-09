from langchain_google_genai import GoogleGenerativeAI
from langchain_community.document_loaders.recursive_url_loader import RecursiveUrlLoader
from bs4 import BeautifulSoup as Soup
import re

llm = GoogleGenerativeAI(model="gemini-pro")

def get_article(page):
   new_page = re.sub('<br />','  ', page)
   article = Soup(new_page, "html.parser").find('article')
   if article:
       return(article.get_text())

loader = RecursiveUrlLoader(
             url = "https://pdx.edu/computer-science/contact",
             max_depth = 2,
             extractor=lambda x: get_article(x)
)

docs = loader.load()
print(len(docs))
for d in docs:
  print(d.metadata)
  print(d.page_content)
