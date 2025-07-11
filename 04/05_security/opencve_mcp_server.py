from fastmcp import FastMCP, Context
import requests
import os

mcp = FastMCP("OpenCVE")

test_r = requests.get(
        f"https://app.opencve.io/api/cve?page=1",
        auth=(os.getenv("OPENCVE_USERNAME"), os.getenv("OPENCVE_PASSWORD")),
    )

if test_r.status_code != 200:
    raise Exception("OpenCVE API is not reachable. Please check your OPENCVE_USERNAME and OPENCVE_PASSWORD environment variables.")

@mcp.tool("search_cve")
async def search_cve(query: str, page: int, ctx: Context = None):
    """
    Search for a CVE via keyword, or description. Returns up to 10 results per page in JSON format.
    """
    r = requests.get(
        f"https://app.opencve.io/api/cve?page={page}&search={query}",
        auth=(os.getenv("OPENCVE_USERNAME"), os.getenv("OPENCVE_PASSWORD")),
    )
    return r.json()["results"]

@mcp.resource(uri="cve://latest",
              mime_type="application/json",
              name="Latest CVEs",
              description="Provides the latest CVEs from OpenCVE.")
def get_latest_cves(ctx: Context):
    """
    Get the latest CVEs from OpenCVE.
    """
    r = requests.get(
        "https://app.opencve.io/api/cve?page=1",
        auth=(os.getenv("OPENCVE_USERNAME"), os.getenv("OPENCVE_PASSWORD")),
    )
    return r.json()["results"]

@mcp.tool("get_cve")
def get_cve(cve_id: str, ctx: Context):
    """
    Provides information on the provided CVE ID. Returns JSON.
    """
    r = requests.get(
        f"https://app.opencve.io/api/cve/{cve_id}",
        auth=(os.getenv("OPENCVE_USERNAME"), os.getenv("OPENCVE_PASSWORD")),
    )
    return r.json()


if __name__ == "__main__":
    mcp.run(transport="stdio")
