from fastmcp import FastMCP
import subprocess
import sys

mcp = FastMCP("Command")

@mcp.tool("command")
async def command(command):
    """Runs an arbitrary Linux command"""
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return(result.stdout)

if __name__ == "__main__":
    if sys.argv[1] == 'stdio':
        mcp.run(transport="stdio")
    else:
        mcp.run(transport="http", host="0.0.0.0", port=8080)

