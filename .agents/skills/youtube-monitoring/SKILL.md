---
name: youtube-monitoring
description: "YouTube monitoring and analysis pipeline for extracting transcripts, metadata, insights, trends, and structured reports. Use when the task is to analyze a YouTube video, playlist, or channel for relevance, insights, or knowledge-base updates via the provided scripts or MCP server. Do NOT use for generic media downloads, format conversion, playback issues, or non-YouTube platforms."
---

# Youtube Monitoring

## Overview
Analyze YouTube content for relevance, insights, trends, and produce structured reports and a local knowledge base. The workflow uses yt-dlp for data collection and supports Gemini or Anthropic for analysis.

## Quick Start
Run the analysis script on a video, playlist, or channel URL:

```bash
python scripts/skill.py "https://youtube.com/playlist?list=..." "ai-agents, automation, llm"
```

Example with Gemini:

```bash
set LLM_PROVIDER=gemini
set GEMINI_API_KEY=YOUR_KEY
python scripts/skill.py "https://youtube.com/watch?v=..." "ai-agents, automation"
```

Example with Anthropic:

```bash
set LLM_PROVIDER=anthropic
set ANTHROPIC_API_KEY=YOUR_KEY
python scripts/skill.py "https://youtube.com/watch?v=..." "ai-agents, automation"
```

Run the MCP-compatible HTTP server:

```bash
python scripts/mcp_server.py --port 8765
```

## Inputs
- URL: YouTube video, playlist, or channel
- Criteria: comma-separated topics of interest
- Optional filters: min_score, max_videos, self_improve

## Outputs
- JSON report and Markdown report in `scripts/reports/`
- Knowledge base in `scripts/knowledge_base/knowledge_base.json`
- Logs in `scripts/logs/`

## Workflow
1. Collect video URLs from the source URL using yt-dlp.
2. Download metadata, transcripts, and top comments.
3. Analyze relevance and extract insights, trends, and actionable ideas.
4. Generate a JSON and Markdown report.
5. Update the local knowledge base.

## MCP Server
Endpoints are served by `scripts/mcp_server.py`:
- POST `/analyze` start analysis in background
- POST `/analyze/sync` run analysis synchronously
- GET `/reports` list recent reports
- GET `/report/{id}` fetch a report
- GET `/knowledge-base` fetch knowledge base
- GET `/health` health check
- POST `/improve` read improvement suggestions

## Environment
- `LLM_PROVIDER` optional, default `gemini` (`gemini` or `anthropic`)
- `GEMINI_API_KEY` or `GOOGLE_API_KEY` required for `LLM_PROVIDER=gemini`
- `ANTHROPIC_API_KEY` required for `LLM_PROVIDER=anthropic`
- `GEMINI_MODEL` optional, default `gemini-2.5-pro`
- `ANTHROPIC_MODEL` optional, default `claude-opus-4-6`
- `YOUTUBE_API_KEY` optional (Data API v3)

## Common Mistakes
- Missing provider API key causes analysis failures.
- Wrong `LLM_PROVIDER` value causes startup failure.
- Very long transcripts may require limiting `max_videos`.
- Using non-YouTube URLs should be rejected at the trigger stage.
