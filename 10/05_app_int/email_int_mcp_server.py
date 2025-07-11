from fastmcp import FastMCP
import requests
import os

OPENCVE_USERNAME = os.getenv('OPENCVE_USERNAME')
OPENCVE_PASSWORD = os.getenv('OPENCVE_PASSWORD')
mcp = FastMCP("App Intelligence")

# Define OpenCVE API tools
class CVE_ID(BaseModel):
    cve_id: str = Field(description="Should be a CVE ID such as CVE-2022-1234")
    @model_validator(mode="before")
    def is_valid_cve_id(cls, values: dict[str,any]) -> dict[str,any]:
        cve_pattern = re.compile(r'^CVE-\d{4}-\d{4,}$')
        if cve_pattern.match(values.get("cve_id")):
            return values
        raise ValueError("Malformed CVE ID")

@tool("cve_by_id", args_schema=CVE_ID, return_direct=False)
def cve_by_id(cve_id):
    """Lookup CVE given its ID"""
    url = f'https://app.opencve.io/api/cve/{cve_id}'
    response = requests.get(url, auth=(OPENCVE_USERNAME, OPENCVE_PASSWORD))
    if response.status_code == 200:
        return response.json()

class CWE_ID(BaseModel):
    cwe_id: str = Field(description="Should be a CWE ID such as CWE-123")
    @model_validator(mode="before")
    def is_valid_cwe_id(cls, values: dict[str,any]) -> dict[str,any]:
        cwe_pattern = re.compile(r'^CWE-\d{1,}$')
        if cwe_pattern.match(values.get("cwe_id")):
            return values
        raise ValueError("Malformed CWE ID")
    
@tool("cwe_by_id", args_schema=CWE_ID, return_direct=False)
def cwe_by_id(cwe_id):
    """Lookup weaknesses and CWE given its ID"""
    url = f'https://app.opencve.io/api/weaknesses/{cwe_id}'
    response = requests.get(url, auth=(OPENCVE_USERNAME, OPENCVE_PASSWORD))
    if response.status_code == 200:
        return response.json()

if __name__ == "__main__":
    if sys.argv[1] == 'stdio':
        mcp.run(transport="stdio")
    else:
        mcp.run(transport="http", host="0.0.0.0", port=8080)
