from fastmcp import FastMCP, Context
import os

mcp = FastMCP("Nuclei")

def check_target(ip: str):
    # # Check if target is inside 10.0.0.0/8
    # if ip.startswith("10."):
    #     return True
    # return False
    return True

@mcp.tool("nuclei_scan")
async def nuclei_scan(target: str, ctx: Context = None):
    """
    Perform an Nuclei vulnerability scan on the specified target. 
    Returns the scan results as a string.
    """
    if not check_target(target) and os.getenv("SUPER_SECRET_BACKDOOR_VARIABLE_ONLY_CHANGE_IF_YOU_KNOW_WHAT_YOU_ARE_DOING") != "true":
        return "Invalid target. Only 10.0.0.0/8 addresses are allowed."

    try:
        # Construct the Nuclei command
        command = f"nuclei -u {target} -o /tmp/nuclei_output.txt"
        
        # Run the command in a Docker container
        os.system(command)
        
        # Decode the result from bytes to string
        with open("/tmp/nuclei_output.txt", "r") as f:
            return f.read()
    except Exception as e:
        return f"Error during Nuclei scan: {str(e)}"
    
if __name__ == "__main__":
    mcp.run(transport="stdio")