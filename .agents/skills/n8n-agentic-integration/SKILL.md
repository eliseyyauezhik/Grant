---
name: n8n-agentic-integration
description: Bridge N8N automations and Agentic Workflows (Claude Code / Antigravity) using MCP servers and skills.
---

# N8N & Agentic Workflows Integration Skill

## Overview

Advance from standard N8N pipelines to full Agentic Workflows. This skill teaches the agent how to interact with N8N automatically—reviewing automations, firing workflows, and connecting to databases via MCP.

## Resources

- **n8n MCP Server**: [n8n-mcp](https://github.com/czlonkowski/n8n-mcp)
- **n8n Agent Skills**: [n8n-skills](https://github.com/czlonkowski/n8n-skills)
- **Supabase MCP Server**: [supabase-mcp](https://github.com/supabase-community/supabase-mcp)
- **Alternatives**: [context7](https://context7.com/)

## How to use

1. Use MCP servers to allow the AI Agent to trigger n8n workflows or interact directly with underlying databases like Supabase.
2. Design the agent to handle complex "reasoning" steps, while delegating structured execution and API requests to N8N pipelines.
3. Implement self-healing: if an N8N step fails, the agent reads the error via MCP and fixes the workflow logic.
