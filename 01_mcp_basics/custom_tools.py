"""
01_mcp_basics/custom_tools.py
------------------------------
This file demonstrates how to define Tools, Resources, and Prompts in FastMCP.

Key Concepts:
- @mcp.tool(): Exposes a Python function as a tool the LLM can invoke.
  FastMCP uses type hints & docstrings to construct the JSON schema for the LLM.
- @mcp.resource(): Exposes dynamic/static text or data context to the LLM.
- @mcp.prompt(): Provides reusable prompt templates to guide LLM interactions.
"""

from mcp.server.mcpserver import MCPServer

# Initialize MCP server (mcp 2.x uses MCPServer)
mcp = MCPServer("AdvancedDemoServer")


# ==========================================
# 1. DEFINING TOOLS (@mcp.tool)
# ==========================================

@mcp.tool()
def add_numbers(a: float, b: float) -> float:
    """Add two numbers together.
    
    Args:
        a: First number
        b: Second number
    """
    return a + b


@mcp.tool()
def format_greeting(name: str, title: str = "Developer") -> str:
    """Create a customized greeting string.
    
    Args:
        name: Name of the person to greet
        title: Professional title (default: Developer)
    """
    return f"Hello {title} {name}! Welcome to Model Context Protocol (MCP)."


@mcp.tool()
def get_live_weather(city: str) -> str:
    """Fetch real-time weather information for any city using a live public API.
    
    Args:
        city: Name of the city (e.g., 'Mumbai', 'London', 'New York')
    """
    import urllib.request
    import urllib.parse

    try:
        encoded_city = urllib.parse.quote(city)
        url = f"https://wttr.in/{encoded_city}?format=3"
        req = urllib.request.Request(url, headers={"User-Agent": "curl/7.68.0"})
        with urllib.request.urlopen(req, timeout=5) as response:
            weather_text = response.read().decode("utf-8").strip()
            return f"Live Report: {weather_text}"
    except Exception as e:
        return f"Could not fetch weather for {city}: {str(e)}"


# ==========================================
# 2. DEFINING RESOURCES (@mcp.resource)
# ==========================================

# A) Direct Static URI Resource
@mcp.resource("config://app-settings")
def get_app_settings() -> str:
    """Provides application configuration context to the LLM."""
    return """
    {
        "app_name": "MCP Learning Suite",
        "version": "1.0.0",
        "environment": "development",
        "supported_features": ["tools", "resources", "prompts"]
    }
    """


# B) Dynamic Resource Template (with path parameter)
@mcp.resource("users://{user_id}/profile")
def get_user_profile(user_id: str) -> str:
    """Fetches user profile information dynamically based on user_id URI template."""
    return f"""
    {{
        "user_id": "{user_id}",
        "status": "active",
        "role": "Learner",
        "enrolled_courses": ["MCP 101", "RAG Mastery", "Agentic Frameworks"]
    }}
    """


# ==========================================
# 3. DEFINING PROMPTS (@mcp.prompt)
# ==========================================

@mcp.prompt()
def explain_code_prompt(code_snippet: str) -> str:
    """Generates a structured prompt asking the LLM to explain a code snippet."""
    return f"""Please analyze the following Python code snippet step by step:
1. Explain what the code does.
2. Highlight any potential performance or security risks.
3. Suggest clean code improvements.

Code:
```python
{code_snippet}
```
"""


if __name__ == "__main__":
    # Runs the server using standard input/output (stdio) transport
    # Note: Do NOT print to stdout when running over stdio transport!
    # stdout is reserved exclusively for JSON-RPC messages.
    import sys
    sys.stderr.write("Starting AdvancedDemoServer over stdio...\n")
    mcp.run()
