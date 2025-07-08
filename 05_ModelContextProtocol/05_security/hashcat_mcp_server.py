from fastmcp import FastMCP, Context
import os

mcp = FastMCP("Hashcat")

@mcp.tool("hashcat_dictionary")
async def hashcat_dictionary(hash: str, wordlist: str, hash_type: int, ctx: Context = None):
    """
    Crack a hash using Hashcat with the specified wordlist.
    Returns the cracked password or an error message.
    Avaliable wordlists are the default Kali Linux wordlists in /usr/share/wordlists.
    Example usage:
    hashcat_dictionary("5f4dcc3b5aa765d61d8327ce8f9c5b2", "/usr/share/wordlists/rockyou.txt", 0)
    Where 0 is the hash type for MD5.
    """
    try:
        command = f"hashcat -m {hash_type} {hash} {wordlist} --show -o /tmp/hashcat_output.txt"
        # Sanatize
        command = command.replace(";", "").replace("&", "").replace("|", "")
        os.system(command)
        
        with open("/tmp/hashcat_output.txt", "r") as f:
            return f.read()
    except Exception as e:
        return f"Error during Hashcat crack: {str(e)}"
    
if __name__ == "__main__":
    mcp.run(transport="stdio")