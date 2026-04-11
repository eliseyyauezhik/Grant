---
name: advanced-rag-hybrid-search
description: Implement Hybrid Search and Gemini File Search to drastically improve RAG response accuracy.
---

# Advanced RAG & Hybrid Search Skill

## Overview

Enhance standard RAG implementation by introducing Hybrid Search (combining keyword and vector search) and Reranking with metadata.

## Tools & Resources

- **Techniques**: Hybrid Search, Reranking, Metadata filtering.
- **Tools**: Google Gemini File Search, Pinecone, Supabase pgvector.

## How to use

1. For user queries, do not just rely on vector similarity. Execute a Hybrid Search using both semantic meaning and lexical keywords.
2. Use Metadata (like date, source, author) to pre-filter chunks before sending them to the LLM.
3. Use a Reranker to reorder the top results for maximum accuracy before context generation.
4. For large document repos, leverage Google Gemini's native File Search API to streamline the context window management.
