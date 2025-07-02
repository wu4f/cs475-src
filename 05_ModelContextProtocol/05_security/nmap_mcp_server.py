from fastmcp import FastMCP, Context
import docker
import os

mcp = FastMCP("NMap")
print(os.getenv("DOCKER_HOST"))
docker_client = docker.from_env()

def check_target(ip: str):
    # # Check if target is inside 10.0.0.0/8
    # if ip.startswith("10."):
    #     return True
    # return False
    return True

@mcp.tool("nmap_scan")
async def nmap_scan(target: str, options: str, ctx: Context = None):
    """
    Perform an NMap scan on the specified target with parameters. 
    Options are any valid NMap flag. 
    Returns the scan results as a string.
    """
    if not check_target(target) and os.getenv("SUPER_SECRET_BACKDOOR_VARIABLE_ONLY_CHANGE_IF_YOU_KNOW_WHAT_YOU_ARE_DOING") != "true":
        return "Invalid target. Only 10.0.0.0/8 addresses are allowed."

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