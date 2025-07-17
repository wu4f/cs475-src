from fastmcp import FastMCP
import subprocess
import sys

mcp = FastMCP("Package")

@mcp.tool("list_running_services")
def list_running_services():
    """Retrieves the list of running services on the host"""
    result = subprocess.run(['systemctl', 'list-units', '--type=service', '--state=running'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.stdout

@mcp.tool("list_installed_packages")
def list_installed_packages():
    """Retrieves the list of installed packages and their versions on the host"""
    result = subprocess.run(['dpkg-query', '-W', '-f=${Package} ${Version}\n'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.stdout

@mcp.tool("list_package_vulnerabilities")
def is_package_vulnerable(package_name):
    """Look up vulnerabilities of a package across all versions given the name of the package given as a string.  Find authors of package updates."""
    result = subprocess.run(['apt', 'changelog', package_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.stdout

if __name__ == "__main__":
    if sys.argv[1] == 'stdio':
        mcp.run(transport="stdio")
    else:
        mcp.run(transport="http", host="0.0.0.0", port=8080)
