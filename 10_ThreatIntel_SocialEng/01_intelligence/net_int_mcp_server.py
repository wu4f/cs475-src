from fastmcp import FastMCP
import requests
import os
import sys

VIRUSTOTAL_API_KEY = os.getenv("VIRUSTOTAL_API_KEY")
mcp = FastMCP("Network Intelligence")

@mcp.tool("ip_loc")
async def ip_loc(address:str):
    """(CHANGE ME)"""
    url = f"http://ipwho.is/{address}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()

@mcp.tool("ip_report")
async def ip_report(address:str):
    """(CHANGE ME)"""
    url = f"https://www.virustotal.com/api/v3/ip_addresses/{address}"
    request_headers = {"x-apikey": VIRUSTOTAL_API_KEY}
    response = requests.get(url, headers=request_headers)
    if response.status_code == 200:
        return response.json()

if __name__ == "__main__":
    if sys.argv[1] == 'stdio':
        mcp.run(transport="stdio")
    else:
        mcp.run(transport="http", host="0.0.0.0", port=8080)