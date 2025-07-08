from fastmcp import FastMCP, Context
import docker
import os

mcp = FastMCP("NMap")
docker_client = docker.from_env()

@mcp.tool("nmap_scan")
async def nmap_scan(target: str, options: str, ctx: Context = None):
    """
    Perform an NMap scan on the specified target with parameters.
    Options are any valid NMap flag.
    Full port scans like -p- are time-consuming and resource intensive, avoid usage if possible.
    If you need to scan all ports, please make the scan as efficient as possible by using options like `-sS` for a SYN scan.
    Returns the scan results as a string.
    Example usage:
    nmap_scan("192.168.1.1", "-sC -sV")
    """
    try:
        # Construct the NMap command
        command = f"{options} {target}"

        # Run the command in a Docker container
        result = docker_client.containers.run("instrumentisto/nmap", command, remove=True)

        # Decode the result from bytes to string
        return result.decode('utf-8')
    except Exception as e:
        return f"Error during NMap scan: {str(e)}"


if __name__ == "__main__":
    mcp.run(transport="stdio")
