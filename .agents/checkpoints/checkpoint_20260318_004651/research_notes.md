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
