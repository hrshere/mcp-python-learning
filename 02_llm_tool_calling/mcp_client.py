"""
02_llm_tool_calling/mcp_client.py
----------------------------------
This script demonstrates how an MCP Client:
1. Spawns an MCP Server over stdio transport.
2. Discovers tools available on the server (list_tools).
3. Executes tools programmatically (call_tool).
4. Integrates with an LLM (Gemini API) for end-to-end tool calling.
"""

import asyncio
import os
import sys
from dotenv import load_dotenv

from mcp import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters

load_dotenv()


async def run_mcp_client():
    # 1. Configure the MCP Server parameters to launch our server script
    server_script = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "01_mcp_basics", "custom_tools.py")
    )
    
    server_params = StdioServerParameters(
        command=sys.executable,
        args=[server_script],
        env=os.environ.copy()
    )

    print("🔌 Spawning MCP Server subprocess over stdio...")

    # 2. Connect to the MCP Server over stdio
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize handshake
            await session.initialize()
            print("✅ MCP Session Initialized!")

            # 3. Discover available tools from the server
            tools_result = await session.list_tools()
            print(f"\n🛠 Discovered {len(tools_result.tools)} tools on MCP Server:")
            for tool in tools_result.tools:
                print(f"  • {tool.name}: {tool.description}")

            # 4. Direct Tool Execution Test
            print("\n🧪 Testing Direct Tool Execution: 'get_live_weather(city=\"Mumbai\")'...")
            weather_result = await session.call_tool("get_live_weather", {"city": "Mumbai"})
            print(f"  Result: {weather_result.content[0].text}")

            # 5. LLM Integration (Gemini API optional execution)
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                print("\n💡 Tip: Add GEMINI_API_KEY to your .env file to enable automated LLM tool calling!")
                return

            print("\n🤖 Connecting to Gemini LLM for automated tool calling...")
            from google import genai
            from google.genai import types

            client = genai.Client(api_key=api_key)

            # Convert MCP tools to Gemini function declarations
            function_declarations = []
            for tool in tools_result.tools:
                # Convert tool input schema
                function_declarations.append(
                    types.FunctionDeclaration(
                        name=tool.name,
                        description=tool.description or "",
                        parameters=tool.inputSchema
                    )
                )

            gemini_tools = [types.Tool(function_declarations=function_declarations)]

            # Send prompt to Gemini
            user_prompt = "What is the current weather in Mumbai and add 15 and 27 together?"
            print(f"  User Prompt: '{user_prompt}'")

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=user_prompt,
                config=types.GenerateContentConfig(tools=gemini_tools)
            )

            # Check if Gemini requested function calls
            if response.function_calls:
                for call in response.function_calls:
                    print(f"  🤖 LLM requested tool: {call.name} with args: {call.args}")
                    tool_output = await session.call_tool(call.name, dict(call.args))
                    print(f"  ⚙️ Executed tool on MCP server -> Output: {tool_output.content[0].text}")


if __name__ == "__main__":
    asyncio.run(run_mcp_client())
