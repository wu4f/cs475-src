import requests
from bs4 import BeautifulSoup
from langchain_google_genai import GoogleGenerativeAI, HarmCategory, HarmBlockThreshold

def summarize_url(url):
    llm = GoogleGenerativeAI(model="gemini-1.5-pro-latest",
        safety_settings = {
          HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
        },
        temperature=0
    )
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text()
    else:
        return "Failed to scrape the website"
    prompt = f"Explain the security issue in the following article: {text}"
    response = llm.invoke(prompt)
    return response


# url = "https://krebsonsecurity.com/2024/02/arrests-in-400m-sim-swap-tied-to-heist-at-ftx/"
print("Welcome to my URL summarizer.  Enter a URL about a security incident and I will summarize the security issue it involves.  A blank line exits.")
while True:
    content = input(">> ")
    if content:
        result = summarize_url(content)
        print(result)
    else:
        break
