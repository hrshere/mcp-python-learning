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

> 💡 **Learned**: MCP decouples the tool implementation from the LLM framework. You write tool logic once in Python/FastMCP, and any host or client can use it.
>
> 🔄 **Re-learned**: Python type hints (`int`, `str`, `dict`) and docstrings are not just for code quality—FastMCP uses them to automatically build JSON Schemas that the LLM understands!
>
> ❌ **Unlearned**: LLMs do NOT execute code directly inside their neural network. They output structured text (JSON) requesting a tool execution, and our runtime/MCP server executes it and feeds the result back.
