from mcp.server.mcpserver import MCPServer

# 1. Initialize the MCP Server (mcp 2.x uses MCPServer)
mcp = MCPServer("DemoServer")

# Entry point for running the server via stdio transport
if __name__ == "__main__":
    mcp.run()
