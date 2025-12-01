from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Math")

@mcp.tool()
def multiply(a: int, b: int) -> float:
    """Multiplies the a and b"""
    return a * b

@mcp.tool()
def add(a: int, b: int) -> float:
    """Adds the a and b"""
    return a + b


# The transport="stdio" argument tells the server to:
# use standard input output to recieve and respond to tool function calls

if __name__=="__main__":
    mcp.run(transport="stdio")