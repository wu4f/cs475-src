from fastmcp import FastMCP
import requests
import os
import sys

OPENCVE_USERNAME = os.getenv('OPENCVE_USERNAME')
OPENCVE_PASSWORD = os.getenv('OPENCVE_PASSWORD')
mcp = FastMCP("App Intelligence")

@mcp.tool("cve_by_id")
def cve_by_id(cve_id: str):
    """Lookup CVE given its ID such as CVE-2025-25257"""
    url = f'https://app.opencve.io/api/cve/{cve_id}'
    response = requests.get(url, auth=(OPENCVE_USERNAME, OPENCVE_PASSWORD))
    if response.status_code == 200:
        return response.json()
    
@mcp.tool("cwe_by_id")
def cwe_by_id(cwe_id):
    """Lookup weaknesses and CWE given its ID such as CWE-787"""
    url = f'https://app.opencve.io/api/weaknesses/{cwe_id}'
    response = requests.get(url, auth=(OPENCVE_USERNAME, OPENCVE_PASSWORD))
    if response.status_code == 200:
        return response.json()

if __name__ == "__main__":
    if sys.argv[1] == 'stdio':
        mcp.run(transport="stdio")
    else:
        mcp.run(transport="http", host="0.0.0.0", port=8080)
