from fastmcp import FastMCP, Context
import os
import docker

mcp = FastMCP("Curl")
client = docker.from_env()

@mcp.tool("curl_request")
async def curl_request(options: str, ctx: Context = None):
    """
    Perform a CURL request with the specified command.
    Format `curl [command]`.
    Returns the result of the CURL command as a string.
    """
    try:        
        # Run in Docker
        result = client.containers.run("curlimages/curl", options, remove=True, network_mode="host")
        return result.decode("utf-8")
    except Exception as e:
        return f"Error during CURL request: {str(e)}"
    
if __name__ == "__main__":
    mcp.run(transport="stdio")