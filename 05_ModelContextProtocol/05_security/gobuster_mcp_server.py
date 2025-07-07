from fastmcp import FastMCP, Context
import os

mcp = FastMCP("Gobuster")

@mcp.tool("gobuster_dir")
async def gobuster_dir(url: str, wordlist: str, ctx: Context = None):
    """
    Perform a Gobuster directory scan on the specified URL using the provided wordlist.
    Wordlists are the default Kali Linux wordlists in /usr/share/wordlists.
    You typically want to use /usr/share/wordlists/dirb/big.txt.
    Returns the scan results as a string.
    """
    try:
        command = f"gobuster dir -u {url} -w {wordlist}"
        # Sanatize
        command = command.replace(";", "").replace("&", "").replace("|", "")
        
        os.system(f"{command} -o /tmp/gobuster_output.txt")
        
        with open("/tmp/gobuster_output.txt", "r") as f:
            return f.read()
    except Exception as e:
        return f"Error during Gobuster scan: {str(e)}"
    
if __name__ == "__main__":
    mcp.run(transport="stdio")