from fastmcp import FastMCP, Context
import os

mcp = FastMCP("Filesystem")

@mcp.tool("read_file")
async def read_file(file_path: str, ctx: Context = None):
    """
    Read the contents of a file from the filesystem.
    Returns the file contents as a string.
    """
    try:
        with open(file_path, "r") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"
    
@mcp.tool("write_file")
async def write_file(file_path: str, content: str, ctx: Context = None):
    """
    Write content to a file on the filesystem.
    Returns a success message or an error message.
    """
    try:
        with open(file_path, "w") as f:
            f.write(content)
        return f"Successfully wrote to {file_path}"
    except Exception as e:
        return f"Error writing to file: {str(e)}"
    
@mcp.tool("list_directory")
async def list_directory(directory_path: str, ctx: Context = None):
    """
    List the contents of a directory on the filesystem.
    Returns a list of filenames or an error message.
    """
    try:
        return os.listdir(directory_path)
    except Exception as e:
        return f"Error listing directory: {str(e)}"
    
# Disabled until I can figure out how to stop the LLM from doing anything destructive.
@mcp.tool("delete_file", enabled=False)  
async def delete_file(file_path: str, ctx: Context = None):
    """
    Delete a file from the filesystem.
    Returns a success message or an error message.
    """
    try:
        os.remove(file_path)
        return f"Successfully deleted {file_path}"
    except Exception as e:
        return f"Error deleting file: {str(e)}"
    
if __name__ == "__main__":
    mcp.run(transport="stdio")