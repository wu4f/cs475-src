from fastmcp import FastMCP, Context
import os

mcp = FastMCP("SQLMap")

@mcp.tool("sqlmap_dump_request_file")
async def sqlmap_dump(request_file: str, ctx: Context = None):
    """
    Perform an SQLMap dump on the specified request file.
    File should be passed as a path and contain the full HTTP request.
    Returns the dump results as a string.
    """
    try:
        command = f"sqlmap -r {request_file} --dump -o /tmp/sqlmap_output.txt"
        # Sanatize
        command = command.replace(";", "").replace("&", "").replace("|", "")
        
        os.system(command)
        
        with open("/tmp/sqlmap_output.txt", "r") as f:
            return f.read()
    except Exception as e:
        return f"Error during SQLMap dump: {str(e)}"
    
@mcp.tool("sqlmap_dump_target")
async def sqlmap_dump_target(target: str, ctx: Context = None):
    """
    Perform an SQLMap dump on the specified target URL.
    Returns the dump results as a string.
    """
    try:
        command = f"sqlmap -u {target} --dump -o /tmp/sqlmap_output.txt"
        # Sanatize
        command = command.replace(";", "").replace("&", "").replace("|", "")
        
        os.system(command)
        
        with open("/tmp/sqlmap_output.txt", "r") as f:
            return f.read()
    except Exception as e:
        return f"Error during SQLMap dump: {str(e)}"
    
if __name__ == "__main__":
    mcp.run(transport="stdio")
