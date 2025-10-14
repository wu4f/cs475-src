from fastmcp import FastMCP
import requests
import os
import sys
import subprocess

RAPID_API_KEY = os.getenv("RAPID_API_KEY")
mcp = FastMCP("DNS Intelligence")

@mcp.tool("cert_domain_search")
async def cert_domain_search(domain):
    """(CHANGE ME)"""
    url = f"""https://crt.sh/?Identity={domain}&output=json"""
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()

@mcp.tool("email_domain_search")
async def email_domain_search(domain):
    """(CHANGE ME)"""
    url = "https://mailcheck.p.rapidapi.com/"
    querystring = {"domain": domain}
    request_headers = {
	"X-RapidAPI-Key": RAPID_API_KEY,
	"X-RapidAPI-Host": "mailcheck.p.rapidapi.com"
    }
    response = requests.get(url, headers=request_headers, params=querystring)
    if response.status_code == 200:
        return response.json()

@mcp.tool("whois_domain_search")
async def whois_domain_search(domain:str):
    """(CHANGE ME)"""
    result = subprocess.run(['whois',domain], capture_output=True, text=True, check=True)
    if result:
        return result 
    
if __name__ == "__main__":
    if sys.argv[1] == 'stdio':
        mcp.run(transport="stdio")
    else:
        mcp.run(transport="http", host="0.0.0.0", port=8080)