from mcp.server.fastmcp import FastMCP

# 1. Initialize the MCP Server
# "DemoServer" is the identifier/name of your MCP server.
mcp = FastMCP("DemoServer")

# Entry point for running the server via stdio transport
if __name__ == "__main__":
    mcp.run()
