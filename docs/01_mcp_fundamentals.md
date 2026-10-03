# 📗 Journal 01: MCP (Model Context Protocol) Fundamentals

## 1. What is MCP?
**Model Context Protocol (MCP)** is an open standard created by Anthropic (and widely adopted across the AI ecosystem) that standardizes how LLM applications communicate with external data sources, tools, and context providers.

Think of MCP as **USB-C for AI Applications**:
- Before USB-C, every device had custom connectors.
- Before MCP, every LLM framework (LangChain, LlamaIndex, custom code) wrote custom integration code for every API or database.
- With MCP, an **MCP Server** exposes tools/resources once, and any **MCP Client** (Claude Desktop, Antigravity IDE, custom LLM scripts) can plug in and interact seamlessly.

---

## 2. Core Concepts of MCP

An MCP Server provides 3 core primitives:

| Primitive | Description | Example |
| :--- | :--- | :--- |
| **Tools** | Executable functions that LLMs can call to perform actions or computations. | `get_weather(city)`, `query_database(sql)`, `run_code(script)` |
| **Resources** | Readable data feeds or documents exposed to the LLM as context. | `file://config.json`, `db://users/active`, `log://live` |
| **Prompts** | Pre-designed prompt templates and reusable instruction contexts. | `analyze_code_bug(snippet)`, `summarize_paper(pdf)` |

---

## 3. How Transports Work
MCP supports two primary transport methods for client-server communication:
1. **Stdio (Standard Input/Output)**: The client launches the server as a local subprocess and communicates via JSON-RPC over stdin/stdout. Ideal for local development & CLI tools.
2. **SSE (Server-Sent Events)**: Communicates over HTTP with SSE for server-to-client updates and POST requests for client-to-server messages. Ideal for remote/cloud servers.

---

## 4. Learn, Re-learn & Unlearn Log

> 💡 **Learned**: 
> - **Decoupled Tools**: MCP decouples tool implementation from the LLM framework. You write tool logic once in Python, and any client (Claude Desktop, IDEs, custom apps) can consume it.
> - **Resources (URIs vs Templates)**: Direct URIs (`config://app-settings`) provide static background context, while Resource Templates (`users://{user_id}/profile`) allow dynamic parameterized context.
> - **Multi-Server Architecture**: An AI Client can aggregate tools, resources, and prompts from multiple specialized MCP servers simultaneously (e.g. Database Server + Slack Server + RAG Server).
>
> 🔄 **Re-learned**: 
> - **SDK v2.x Migration**: In Python `mcp` SDK 2.x, `FastMCP` was renamed to `MCPServer` (`from mcp.server.mcpserver import MCPServer`).
> - **Type Hint Schemas**: Python type hints (`str`, `float`) and docstrings aren't just comments—MCPServer automatically turns them into JSON Schemas for the LLM!
> - **Stdio Transport**: `mcp.run()` runs a continuous standard I/O loop expecting JSON-RPC messages from a host client, which is why running it manually hangs waiting for input.
>
> ❌ **Unlearned**: 
> - LLMs do NOT execute Python code directly inside their neural network. They emit structured JSON requests asking an MCP server to execute the tool and return the output.
