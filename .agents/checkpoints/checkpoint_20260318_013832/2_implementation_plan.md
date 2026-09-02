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

## 2026-03-18 - Skill System Refactor

Objective
- Remove stale operational rules from the remaining local skills and centralize shared workspace policy in a dedicated skill.

Target files
- `AGENTS.md`
- `.agents/skills/core-agent-rules/SKILL.md`
- `.agents/skills/task-executor/SKILL.md`
- `.agents/skills/safety-guardrails/SKILL.md`
- `.agents/skills/skill-conductor/SKILL.md`
- `.agents/skills/version-control/SKILL.md`
- `research_notes.md`
- `implementation_plan.md`
- `task.md`

Plan steps
1. Review all local `SKILL.md` files and identify only the ones with stale paths or duplicated workspace policy.
2. Create `core-agent-rules` as a concise shared policy skill.
3. Update the system skills to reference `core-agent-rules` and trim duplicated rules.
4. Fix `version-control` so it matches the current tool model and rollback safety expectations.
5. Validate the changed skills and log the Tier 2 actions in `agent_audit.log`.

Verification
- Re-read the changed skills for internal consistency.
- Run `quick_validate.py` on each edited or newly created skill.
- Search the skill tree for remaining stale path patterns and obsolete `run_command` references.

## 2026-03-18 - Global Skill Mirror And Commit

Objective
- Bring the global skill set in `C:\Users\Admin\.agents\skills` up to the same system-policy baseline and create a dedicated local commit for the refactor.

Target areas
- `C:\Users\Admin\.agents\skills\core-agent-rules\SKILL.md`
- `C:\Users\Admin\.agents\skills\task-executor\SKILL.md`
- `C:\Users\Admin\.agents\skills\safety-guardrails\SKILL.md`
- `C:\Users\Admin\.agents\skills\skill-conductor\SKILL.md`
- Local git commit containing only:
  - `AGENTS.md`
  - `.agents/skills/core-agent-rules/SKILL.md`
  - `.agents/skills/task-executor/SKILL.md`
  - `.agents/skills/safety-guardrails/SKILL.md`
  - `.agents/skills/skill-conductor/SKILL.md`
  - `.agents/skills/version-control/SKILL.md`
  - `research_notes.md`
  - `implementation_plan.md`
  - `task.md`
  - `agent_audit.log`

Plan steps
1. Back up the existing global system skill files.
2. Add a generic global `core-agent-rules`.
3. Update the global system skills to reference it and remove stale legacy rules.
4. Validate the global skills and re-run the stale-pattern search.
5. Stage only the local refactor files and create a dedicated git commit.

Verification
- `quick_validate.py` passes for all changed global skills.
- Legacy-pattern search in `C:\Users\Admin\.agents\skills` returns clean.
- `git status --short` after commit shows no unintended staged files from unrelated work.

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

## 2026-03-18 - NotebookLM MCP Auto Refresh

Objective
- Stabilize the local NotebookLM workflow so tokens can be refreshed from Chrome DevTools and then reused by `nlm` and MCP through the configured proxy.

Target files
- `notebooklm_auto_refresh.py`
- `launch_notebooklm_debug_chrome.ps1`
- `refresh_notebooklm_tokens.ps1`
- `run_nlm_proxy.ps1`
- `research_notes.md`
- `implementation_plan.md`
- `task.md`

Plan
1. Repair `notebooklm_auto_refresh.py` syntax, messages, and DevTools flow — risk: LOW
2. Add a Chrome launcher that reuses proxy settings from `mcp_config.json` and enables remote debugging — risk: LOW
3. Add a thin `nlm` wrapper that reuses proxy env from `mcp_config.json` — risk: LOW
4. Append NotebookLM-specific workflow notes instead of replacing unrelated artifact history — risk: LOW
5. Verify Python syntax, script help output, and launcher/wrapper dry runs locally — risk: MEDIUM
6. Perform one live refresh and re-run `nlm notebook get` for both notebook IDs after the user launches Chrome — risk: MEDIUM

Verification
- `python -m py_compile notebooklm_auto_refresh.py`
- `python notebooklm_auto_refresh.py --help`
- `powershell -File launch_notebooklm_debug_chrome.ps1 -PrintOnly`
- `powershell -File run_nlm_proxy.ps1 --help`

## 2026-03-18 - Cross-Update Stabilization Plan

Objective
- Reconcile overlapping updates across rules, skills, vault instructions, workflow artifacts, and pending local changes before further feature work.

Execution order
1. Governance cleanup — risk: MEDIUM
   - Align `AGENTS.md`, `implementation_plan.md`, `task.md`, and KB-vault instructions on the actual `workspace/` model.
   - Explicitly define whether `.obsidian/` is an allowed vault exception.
   - Update KB verification statements so they reflect the unresolved setup steps.
2. Artifact correction — risk: LOW
   - Refresh the `youtube-monitoring` sections in `research_notes.md`, `implementation_plan.md`, and `task.md` to match the current Gemini/Anthropic implementation and actual file names.
   - Separate "implemented", "verified", and "still pending" states more clearly.
3. Change-boundary hardening — risk: MEDIUM
   - Define the authority rule between local `.agents/skills/**` and `C:\Users\Admin\.agents\skills\`.
   - Improve `agent_audit.log` write discipline so each action is newline-safe and parseable.
   - Group pending uncommitted work into themed checkpoints before additional edits.
4. Feature continuation — risk: MEDIUM
   - Implement LLM fallback behavior only after the governance and artifact layer is internally consistent.
   - Integrate `youtube-monitoring` with the monitoring service only after commit boundaries and source-of-truth rules are explicit.

Verification
- Re-read the reconciled rules and confirm there is no contradiction between root rules and `workspace/` rules.
- Verify all workflow artifacts describe the current code and current completion state.
- Re-run `quick_validate.py` for changed skills if any system-skill text is edited.
- Confirm `git status --short` can be explained by themed work items rather than mixed incidental drift.
