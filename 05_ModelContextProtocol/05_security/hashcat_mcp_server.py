from fastmcp import FastMCP, Context
import os

mcp = FastMCP("Hashcat")

@mcp.tool("hashcat_dictionary")
async def hashcat_dictionary(hash: str, wordlist: str, hash_type: int, ctx: Context = None):
    """
    Crack a hash using Hashcat with the specified wordlist.
    Returns the cracked password or an error message.
    Avaliable wordlists are the default Kali Linux wordlists in /usr/share/wordlists.
    """
    try:
        command = f"hashcat -m {hash_type} {hash} {wordlist} --show"
        os.system(command)
        
        with open("/tmp/hashcat_output.txt", "r") as f:
            return f.read()
    except Exception as e:
        return f"Error during Hashcat crack: {str(e)}"
    
if __name__ == "__main__":
    mcp.run(transport="stdio")