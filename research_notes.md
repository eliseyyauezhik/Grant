# Research Notes

Goal
- Create a new skill in .agents/skills based on YT_Analyzer_v1 for YouTube monitoring and analysis.

Source assets
- F:\ДИМА\ПРОЕКТЫ\ютюб скилл\skill.py
- F:\ДИМА\ПРОЕКТЫ\ютюб скилл\mcp_server.py
- F:\ДИМА\ПРОЕКТЫ\ютюб скилл\requirements.txt
- F:\ДИМА\ПРОЕКТЫ\ютюб скилл\SKILL.md

Observed capabilities
- yt-dlp pipeline for playlist/channel/video URL expansion, transcripts, metadata, comments
- AI analysis via Anthropic (claude-opus-4-6)
- Report JSON and Markdown saved to reports directory
- Knowledge base stored in knowledge_base.json
- Self-improvement suggestions saved to logs
- MCP HTTP server endpoints: /analyze, /analyze/sync, /reports, /report/{id}, /knowledge-base, /health, /improve

Dependencies and env
- anthropic>=0.40.0
- yt-dlp>=2024.1.0
- ANTHROPIC_API_KEY required
- YOUTUBE_API_KEY optional (Data API v3)

Trigger definition (initial)
- Trigger when the user asks to analyze a YouTube video, playlist, or channel for relevance, insights, trends, and a structured report or knowledge-base update.
- Do not trigger for generic download, conversion, playback issues, or non-YouTube platforms.

Baseline (without skill)
- The agent lacks built-in knowledge of the YT_Analyzer_v1 pipeline and MCP entrypoints, so it would need manual discovery to perform the workflow.

Risks and constraints
- External API keys must never be logged or printed
- Large transcripts require chunking and can hit token limits
- yt-dlp failures and rate limits need retry handling

## 2026-03-17 - Agent System Settings Review

Goal
- Review `D:\ЯндексДиск\Yandex.Disk\ПРОЕКТЫ\KnowledgeBase\.obsidian\AGENTS_ANTIGRAVITY.md`, compare it with the current project agent settings, and improve the local system instructions where it makes sense.

Files inspected
- `AGENTS.md`
- `.agents/skills/task-executor/SKILL.md`
- `.agents/skills/safety-guardrails/SKILL.md`
- `.agents/skills/version-control/SKILL.md`
- `d:\ЯндексДиск\Yandex.Disk\ПРОЕКТЫ\AI_Workspace\KnowledgeBase\available_tools.md`
- `D:\ЯндексДиск\Yandex.Disk\ПРОЕКТЫ\KnowledgeBase\.obsidian\AGENTS_ANTIGRAVITY.md`

Findings
- The external Antigravity file is stronger on operational behavior: inspect the directory first, act instead of only explaining, keep artifacts in Markdown, and constrain clarifying questions.
- The current project `AGENTS.md` is stronger on RPI discipline, testing, and explicit user approvals, but it lacks context-building rules and operational guidance for safe system-setting changes.
- `task-executor` was too rigid for the current collaboration mode because it always waited for approval and still contained irrelevant voice-specific instructions.
- `safety-guardrails` contained outdated project boundaries from another workspace and did not reflect sandbox-first execution or current writable roots.
- Obsidian-specific actions from the external file are useful as principles, but they should not be copied literally into this repository because the current project is not guaranteed to expose Obsidian CLI workflows.

Edge cases and risks
- Existing workflow artifacts already contain notes from another task, so the safest approach is to append dated sections rather than overwrite them.
- Agent-system files are sensitive; they should be checkpointed before edits and summarized explicitly after modification.
- Overfitting the local rules to Obsidian-specific automation would create false expectations for future sessions.

## 2026-03-18 - Skill System Refactor

Goal
- Review the remaining local skills, remove outdated path or workflow references, and extract shared operational policy into a dedicated `core-agent-rules` skill.

Skills reviewed
- `.agents/skills/advanced-rag-hybrid-search/SKILL.md`
- `.agents/skills/docling-document-parsing/SKILL.md`
- `.agents/skills/last-30-days-research/SKILL.md`
- `.agents/skills/n8n-agentic-integration/SKILL.md`
- `.agents/skills/safety-guardrails/SKILL.md`
- `.agents/skills/skill-conductor/SKILL.md`
- `.agents/skills/task-executor/SKILL.md`
- `.agents/skills/version-control/SKILL.md`
- `.agents/skills/vibe-coding-ui/SKILL.md`
- `.agents/skills/youtube-monitoring/SKILL.md`

Findings
- Most domain skills did not contain workspace-specific paths or stale local rules and did not need edits.
- `version-control` still referenced a nonexistent `run_command` tool and lacked an explicit boundary against rolling back unrelated user changes.
- `task-executor`, `safety-guardrails`, and `skill-conductor` all contained shared workspace policy that should live in one place.
- The correct refactor target is a small shared skill, not another expansion of `AGENTS.md`, because the duplication problem exists between multiple skills.

Refactor decisions
- Create `.agents/skills/core-agent-rules/SKILL.md` as the shared policy layer for context scan, writable roots, approvals, artifact hygiene, checkpoint expectations, and audit logging.
- Update system skills to reference `core-agent-rules` and keep only task-specific instructions in their own bodies.
- Leave domain skills unchanged when they contain no stale paths or local policy drift.

## 2026-03-18 - Global Skill Mirror And Commit

Goal
- Mirror the system-skill cleanup into `C:\Users\Admin\.agents\skills` and prepare a separate git commit containing only the local system-skill refactor.

Global findings
- The global skill set contained stale `task-executor`, `safety-guardrails`, and `skill-conductor`.
- The global skill set had no `core-agent-rules` directory.
- The global `safety-guardrails` still contained hardcoded legacy paths from another workspace.
- The global skill set also has no `version-control`; that skill was not copied automatically because its current scripts are repository-anchored and need a separate portability pass.

Actions taken
- Backed up the previous global system skills to `C:\Users\Admin\.agents\skill_backups\20260318_005543`.
- Created `C:\Users\Admin\.agents\skills\core-agent-rules\SKILL.md`.
- Updated the global `task-executor`, `safety-guardrails`, and `skill-conductor` to reference `core-agent-rules` and use generic workspace wording.
- Validated all four global skills with `quick_validate.py`.
- Confirmed a clean legacy-pattern search across `C:\Users\Admin\.agents\skills`.

## 2026-03-18 - KB Vault Implementation

Goal
- Implement a local Obsidian-compatible workspace for the knowledge base and adapt the repository rules to it without mixing binaries into the note graph.

Facts discovered
- The repository did not contain a dedicated `workspace/` vault before implementation.
- `kb_agent_instructions.docx` requires one shared vault directory, Markdown-only storage, reusable skills/templates, and graph-aware navigation.
- `obsidian` CLI is not currently installed or not available in PATH in this environment.
- The repository root contains many non-Markdown artifacts, so using the root as a vault would violate the document's constraints.

Implementation choices
- Create a separate vault in `workspace/` inside the repository.
- Keep new KB content in Markdown only and reserve `workspace/_assets_bin/` for binary exceptions.
- Encode CLI-dependent behavior as conditional rules with a fallback to wikilinks and regular search.

Risks and mitigations
- Obsidian CLI commands cannot be verified end-to-end until the CLI is installed; mitigate by documenting the exact setup steps in `workspace/notes/setup-checklist.md`.
- Existing unrelated repository changes must remain untouched; limit edits to `workspace/` and the root instruction artifacts required by the task.

## 2026-03-18 - NotebookLM MCP Auto Refresh

Goal
- Make NotebookLM MCP usable without manual cURL export each time by refreshing auth from a live Chrome session.

Scope
- `C:\Users\Admin\.gemini\antigravity\mcp_config.json`
- `notebooklm_auto_refresh.py`
- local helper scripts for Chrome launch, token refresh, and proxy-wrapped `nlm`
- NotebookLM CLI storage at `C:\Users\Admin\.notebooklm-mcp-cli\`

Confirmed findings
- `notebooklm-mcp` is already routed through the US proxy in `mcp_config.json`.
- NotebookLM requests from the local RU IP fail with `REGION_NOT_SUPPORTED`.
- Fresh browser tokens captured through the proxy allow `nlm notebook list` to return the expected notebook IDs.
- The short-lived `at` token expires quickly enough to break later `nlm notebook get` calls with `Authentication expired`.
- The initial `notebooklm_auto_refresh.py` file was broken by encoding corruption and a Python syntax error, so it had to be repaired before live validation.

Operational risks
- Auto-refresh still depends on a real Chrome session that is logged into NotebookLM and started with `--remote-debugging-port`.
- Proxy credentials are already stored outside the workspace in `mcp_config.json`; duplicating them inside repo files is unnecessary and should be avoided.
- CLI checks after refresh must still run through the proxy or NotebookLM will fall back to the blocked RU region.
