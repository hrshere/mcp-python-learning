# Module 03: RAG Pipeline with Pinecone Vector DB

In this module, we build an end-to-end RAG (Retrieval-Augmented Generation) pipeline integrated with an MCP tool:

## 🎯 Architecture
1. **Document Ingestion (`ingest.py`)**:
   - Loads custom domain documents.
   - Chunks text recursively into overlapping segments.
   - Generates 768-dimensional embeddings using Gemini `text-embedding-004`.
   - Upserts vectors & text metadata into a **Pinecone Vector Database** serverless index.
2. **MCP RAG Tool (`rag_tool.py`)**:
   - Exposes `@mcp.tool()` `query_knowledge_base(query: str) -> str`.
   - Performs vector similarity search on Pinecone to retrieve top match text chunks.

## 🔑 Environment Setup
Ensure your `.env` contains:
```env
GEMINI_API_KEY=your_gemini_api_key
PINECONE_API_KEY=your_pinecone_api_key
```
