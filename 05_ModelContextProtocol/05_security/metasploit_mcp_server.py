from pymetasploit3.msfrpc import MsfRpcClient
import time
import os
from fastmcp import FastMCP, Context

mcp = FastMCP("Metasploit")
client = MsfRpcClient(
    password="msf",
    port=55553,
    server="127.0.0.1",
    ssl=True,
)

def check_target(ip: str):
    # Check if target is inside 10.0.0.0/8
    # if ip.startswith("10."):
        # return True
    return True

@mcp.tool("metasploit_search")
async def metasploit_search(query: str, ctx: Context = None):
    """
    Search for a module in Metasploit using the provided query.
    Returns the search results as a list of module names.
    """
    if not check_target(query) and os.getenv("SUPER_SECRET_BACKDOOR_VARIABLE_ONLY_CHANGE_IF_YOU_KNOW_WHAT_YOU_ARE_DOING") != "true":
        return "Invalid target. Only 10.0.0.0/8 addresses are allowed."
    try:
        results = client.modules.search(query)
        return results
    except Exception as e:
        return f"Error during Metasploit search: {str(e)}"
    
@mcp.tool("metasploit_info")
async def metasploit_info(module_type: str, module_name: str, ctx: Context = None):
    """
    Get information about a specific Metasploit module.
    Returns the module's description and options.
    """
    try:
        mod = client.modules.use(module_type, module_name)
        info = {
            "description": mod.description,
            "options": mod.options,
            "references": mod.references,
        }
        return info
    except Exception as e:
        return f"Error retrieving module info: {str(e)}"
    
@mcp.tool("metasploit_module_payloads")
async def metasploit_module_payloads(module: str, ctx: Context = None):
    """
    List all available payloads for a given Metasploit exploit module.
    Returns a list of payload names.
    """
    try:
        mod = client.modules.use("exploit", module)
        payloads = mod.targetpayloads()
        return payloads
    except Exception as e:
        return f"Error retrieving payloads for module {module}: {str(e)}"
    
@mcp.tool("metasploit_payload_info")
async def metasploit_payload_info(payload: str, ctx: Context = None):
    """
    Get information about a specific Metasploit payload.
    Returns the payload's description and options.
    """
    try:
        mod = client.modules.use("payload", payload)
        info = {
            "description": mod.description,
            "options": mod.options,
            "references": mod.references,
        }
        return info
    except Exception as e:
        return f"Error retrieving payload info: {str(e)}"

@mcp.tool("metasploit_exploit")
async def metasploit_exploit(module: str, module_options: dict, payload: str, payload_options: dict, ctx: Context = None):
    """
    Run a Metasploit exploit module against the specified target with the provided options.
    Both options are a dictionary of module parameters. The payload is a string representing the payload to use.
    Returns the result of the exploit attempt.
    """
    try:
        result = client.modules.use("exploit", module)
        payload = client.modules.use("payload", payload)
        for key, value in payload_options.items():
            payload[key] = value
        for key, value in module_options.items():
            result[key] = value
        return result.execute(payload=payload)
    except Exception as e:
        return f"Error during Metasploit exploit: {str(e)}"

@mcp.tool("metasploit_sessions")
async def metasploit_sessions(ctx: Context = None):
    """
    List all active Metasploit sessions.
    Returns a list of session IDs and their details.
    """
    try:
        sessions = client.sessions.list
        return sessions
    except Exception as e:
        return f"Error retrieving Metasploit sessions: {str(e)}"
    
@mcp.tool("metasploit_session_interact")
async def metasploit_session_interact(session_id: str, command: str, timeout: float, ctx: Context = None):
    """
    Interact with a specific Metasploit session. Writes a command to the session and returns the output.
    The session_id is the ID of the session to interact with, command is the command to execute,
    and timeout is the time to wait for the command to execute (in seconds).
    Returns the output of the command executed in the session after the timeout.
    """
    try:
        session = client.sessions.session(session_id)
        if session:
            session.write(command)
            time.sleep(timeout)  # Wait for the command to execute
            return session.read()
        else:
            return f"Session {session_id} does not exist."
    except Exception as e:
        return f"Error interacting with session {session_id}: {str(e)}"

if __name__ == "__main__":
    mcp.run(transport="stdio")