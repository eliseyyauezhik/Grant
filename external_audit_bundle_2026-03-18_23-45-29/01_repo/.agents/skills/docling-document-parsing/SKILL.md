---
name: docling-document-parsing
description: Parse and extract complex documents (including images, tables, and graphs) into Markdown for RAG systems using Docling locally.
---

# Docling Document Parsing Skill

## Overview

Use Docling to locally parse any files—especially those with complex structures, images, graphs, and tables—into clean Markdown data. Apply hybrid chunking for improved vectorization.

## Resources

- **Docling Website**: [Docling](https://docling-project.github.io/docling/)
- **Repository**: [Docling RAG Agent](https://github.com/coleam00/ottomator-agents/tree/main/docling-rag-agent)
- **Picture Classification API**: [Docling Picture Classification](https://docling-project.github.io/docling/usage/enrichments/#Picture-classification)

## How to use

1. Process raw PDFs and docx files through Docling to extract pure Markdown.
2. Maintain spatial relationships between text and images/tables during extraction.
3. Apply hybrid chunking before sending data to vector databases (like Pinecone or Supabase).
