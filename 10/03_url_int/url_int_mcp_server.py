from fastmcp import FastMCP
import requests
import os
import sys
import json

VIRUSTOTAL_API_KEY = os.getenv("VIRUSTOTAL_API_KEY")
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
mcp = FastMCP("URL Intelligence")

@mcp.tool("safebrowsing_url_report")
def safebrowsing_url_report(url):
    """(CHANGE ME)"""
    api_url = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={GOOGLE_API_KEY}"
    payload = {
        "client": {
            "clientId": "PSU",  # can be any string
            "clientVersion": "1.0"
        },
        "threatInfo": {
            "threatTypes": [
                "MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE", "POTENTIALLY_HARMFUL_APPLICATION"
            ],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": url}]
        }
    }

    response = requests.post(api_url, json=payload)
    return response.json()

@mcp.tool("virustotal_url_report")
def virustotal_url_report(url):
    """(CHANGE ME)"""
    api_url = f"https://www.virustotal.com/api/v3/urls"
    request_headers = {"x-apikey": VIRUSTOTAL_API_KEY}
    response = requests.post(api_url, headers=request_headers, data={"url":url})
    if response.status_code == 200:
        response_dict = response.json()
        link = response_dict['data']['links']['self']
        response = requests.get(link, headers=request_headers)
        return response.json()

@mcp.tool("phishtank_url_report")
def phishtank_url_report(url):
    """(CHANGE ME)"""
    api_url = f"https://checkurl.phishtank.com/checkurl/"
    payload = { 
                 "format" : "json",
                 "url" : url
    }
    request_headers = {"User-Agent": f"phishtank/{os.getenv('USER')}"}
    response = requests.post(api_url, headers=request_headers, data=payload)
    return response.json()['results']['in_database']

if __name__ == "__main__":
    if sys.argv[1] == 'stdio':
        mcp.run(transport="stdio")
    else:
        mcp.run(transport="http", host="0.0.0.0", port=8080)
