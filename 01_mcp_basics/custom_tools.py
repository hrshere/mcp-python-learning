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

from mcp.server.fastmcp import FastMCP

# Initialize MCP server
mcp = FastMCP("AdvancedDemoServer")


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


# ==========================================
# 2. DEFINING RESOURCES (@mcp.resource)
# ==========================================

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
    print("Starting AdvancedDemoServer...")
    mcp.run()
