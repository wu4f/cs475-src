from fastmcp import FastMCP
import sqlite3

mcp = FastMCP("sqlite")

@mcp.tool()
def query(query: str, path: str) -> str:
    """Query a specified Sqlite3 database. Returns the result of the query."""
    con = sqlite3.connect(path)
    cur = con.cursor()
    res = cur.execute(query)
    con.commit()
    return res.fetchall()

if __name__ == "__main__":
    mcp.run(transport="stdio")