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

## 2026-03-17 - Agent System Settings Review

Objective
- Synchronize the local agent operating rules with the useful parts of `AGENTS_ANTIGRAVITY.md` without importing Obsidian-only assumptions.

Target files
- `AGENTS.md`
- `.agents/skills/task-executor/SKILL.md`
- `.agents/skills/safety-guardrails/SKILL.md`
- `research_notes.md`
- `implementation_plan.md`
- `task.md`

Plan steps
1. Update `AGENTS.md` to add operational priorities, context-scan rules, artifact hygiene, and safer change-management guidance.
2. Refine `task-executor` so it starts with repo inspection, appends to workflow artifacts, and asks for confirmation only when the change is genuinely high risk.
3. Rewrite `safety-guardrails` boundaries to match the current workspace and add sandbox-aware escalation rules.
4. Append the analysis and plan to the existing workflow artifacts instead of replacing previous task notes.
5. Verify the resulting files for internal consistency and log the Tier 2 actions in `agent_audit.log`.

Verification
- Re-read the edited files.
- Check that referenced paths exist and are contextually correct.
- Confirm that the new rules do not require unsupported Obsidian-only commands.

## 2026-03-18 - KB Vault Implementation

Objective
- Build a minimal Obsidian-compatible knowledge-base workspace under `workspace/` and align the root agent rules with that structure.

Execution steps
1. Create `workspace/` subdirectories for `skills/`, `assets/`, `notes/`, `projects/`, and `_assets_bin/`.
2. Add `workspace/agents.md` with Markdown-only, graph-first, and template-first rules.
3. Add minimal templates and Markdown skills for kanban, capture, and review workflows.
4. Convert `kb_agent_instructions.docx` into a Markdown note inside `workspace/notes/` and derive a setup checklist from it.
5. Add starter notes for navigation and task intake.
6. Update the root `AGENTS.md` so KB work is explicitly routed to `workspace/`.
7. Verify that `workspace/` contains only Markdown files and that the main notes reference the new skills and templates.

Verification targets
- `workspace/notes/index.md` links to rules, skills, templates, and active project notes.
- No non-Markdown files exist inside `workspace/` except directories.
- Root and vault-specific instructions agree on `workspace/` boundaries and `_assets_bin/`.
