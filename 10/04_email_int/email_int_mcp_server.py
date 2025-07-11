import os
import requests

RAPID_API_KEY = os.getenv("RAPID_API_KEY")

@mcp.tool("oop_spam_search")
def oop_spam_search(content):
    """(CHANGE ME)"""
    url = "https://oopspam.p.rapidapi.com/v1/spamdetection"

    payload = {
        "content": content,
        "allowedLanguages": ["en"]
    }
    request_headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "oopspam.p.rapidapi.com"
    }
    response = requests.post(url, json=payload, headers=request_headers)
    if response.status_code == 200:
        return response.json()

@mcp.tool("email_is_spammer")
def email_is_spammer(address):
    """(CHANGE ME)"""
    url = f"https://disify.com/api/email/{address}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()