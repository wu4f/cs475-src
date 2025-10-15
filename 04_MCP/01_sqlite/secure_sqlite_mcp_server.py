from fastmcp import FastMCP
import sqlite3
import sys

mcp = FastMCP("sqlite")
con = sqlite3.connect('db_data/metactf_users.db')

@mcp.tool()
async def fetch_users() -> list:
    """Fetch the users in the database.  Takes no arguments and returns a list of users."""
    cur = con.cursor()
    res = cur.execute('SELECT username from USERS')
    return res.fetchall()

@mcp.tool()
async def fetch_users_pass(username: str) -> str:
   """Useful when you want to fetch a password hash for a particular user.  Takes a username as a string argument.  Returns a JSON string"""
   cur = con.cursor()
   res = cur.execute(f"SELECT passhash FROM users WHERE username = '{username}';")
   return res.fetchone()[0]

if __name__ == "__main__":
    if sys.argv[1] == 'stdio':
        mcp.run(transport="stdio")
    else:
        mcp.run(transport="http", host="0.0.0.0", port=8080)
