import requests
from bs4 import BeautifulSoup
from langchain_google_genai import GoogleGenerativeAI

def summarize_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text()
    else:
        return "Failed to scrape the website"
    prompt = f"Explain the security issue in the following article: {text}"
    response = llm.invoke(prompt)
    return response

global llm
llm = GoogleGenerativeAI(model="gemini-pro")

print(summarize_url("https://krebsonsecurity.com/2024/02/arrests-in-400m-sim-swap-tied-to-heist-at-ftx/"))
