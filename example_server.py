#!/usr/bin/env python3
"""
Example MCP server for testing the interactive client.
"""

from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Example Server")


# Add a prompt
@mcp.prompt()
def review_code(code: str, language: str = "python") -> str:
    """Review code and provide feedback."""
    return f"Please review this {language} code:\n\n{code}\n\nProvide feedback on style, logic, and potential improvements."


# Add a static config resource
@mcp.resource("config://app")
def get_config() -> str:
    """Static configuration data"""
    return """{
        "app_name": "Example App",
        "version": "1.0.0",
        "features": ["feature1", "feature2"],
        "debug": false
    }"""


# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}! Welcome to the MCP interactive client."


# Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


# Add a text processing tool
@mcp.tool()
def process_text(text: str, operation: str = "uppercase") -> str:
    """Process text with various operations."""
    if operation == "uppercase":
        return text.upper()
    elif operation == "lowercase":
        return text.lower()
    elif operation == "title":
        return text.title()
    elif operation == "reverse":
        return text[::-1]
    else:
        return f"Unknown operation: {operation}"


# Add a list processing tool
@mcp.tool()
def filter_list(items: list, condition: str = "all") -> list:
    """Filter a list based on conditions."""
    if condition == "all":
        return items
    elif condition == "even":
        return [x for x in items if isinstance(x, (int, float)) and x % 2 == 0]
    elif condition == "odd":
        return [x for x in items if isinstance(x, (int, float)) and x % 2 == 1]
    elif condition == "positive":
        return [x for x in items if isinstance(x, (int, float)) and x > 0]
    else:
        return items


if __name__ == "__main__":
    # Run the server
    mcp.run()
