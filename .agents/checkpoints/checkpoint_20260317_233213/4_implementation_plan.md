# Implementation Plan

Skill name
- youtube-monitoring (kebab-case, <=64 chars)

Stack
- Python
- yt-dlp
- Anthropic API (claude-opus-4-6)
- MCP-compatible HTTP server (BaseHTTPRequestHandler)

Target structure
- .agents/skills/youtube-monitoring/SKILL.md
- .agents/skills/youtube-monitoring/scripts/skill.py
- .agents/skills/youtube-monitoring/scripts/mcp_server.py
- .agents/skills/youtube-monitoring/scripts/requirements.txt
- .agents/skills/youtube-monitoring/references/report_schema.md (optional, only if needed)

External endpoints (from MCP server)
- POST /analyze
- POST /analyze/sync
- GET /reports
- GET /report/{id}
- GET /knowledge-base
- GET /health
- POST /improve

Tests
- Unit tests for pure functions only (no network):
- YTDownloader._extract_id
- YTDownloader._clean_vtt
- ReportGenerator._aggregate_trends and _aggregate_insights
- KnowledgeBase dedup logic

Plan steps
1. Initialize skill scaffold via .agents/skills/skill-conductor/scripts/init_skill.py
2. Copy scripts from source folder into scripts/
3. Rewrite SKILL.md frontmatter and body to meet skill-conductor rules
4. Add minimal references if needed (report schema, env vars)
5. Run quick_validate.py for the new skill
6. Add and run unit tests for non-network logic

Notes
- Keep SKILL.md concise and imperative
- Include triggers and negative triggers in description
- Do not store secrets or API keys in any file
