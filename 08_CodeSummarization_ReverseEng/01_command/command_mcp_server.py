from fastmcp import FastMCP
import subprocess
import sys
import shlex

mcp = FastMCP("Command")

@mcp.tool("command")
async def command(command: str, progress_callback: bool):
    """Runs an arbitrary Linux command"""
    result = subprocess.run(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return(result.stdout.decode('utf-8'))

if __name__ == "__main__":
    if sys.argv[1] == 'stdio':
        mcp.run(transport="stdio")
    else:
        mcp.run(transport="http", host="0.0.0.0", port=8080)

