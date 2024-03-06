import requests
from bs4 import BeautifulSoup
from langchain_google_genai import GoogleGenerativeAI, HarmCategory, HarmBlockThreshold

def summarize_url(llm, url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text()
    else:
        return "Failed to scrape the website"
    prompt = f"Explain the security issue in the following article: {text}"
    response = llm.invoke(prompt)
    return response

llm = GoogleGenerativeAI(
        model = "gemini-pro",
        safety_settings = {
          HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
        }
)

print(summarize_url(llm,"https://krebsonsecurity.com/2024/02/arrests-in-400m-sim-swap-tied-to-heist-at-ftx/"))
