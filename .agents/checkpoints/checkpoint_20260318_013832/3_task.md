# Tasks

- [x] Initialize skill scaffold in .agents/skills/youtube-monitoring
- [x] Copy skill.py, mcp_server.py, requirements.txt into scripts/
- [x] Draft SKILL.md with correct frontmatter and workflow instructions
- [x] Add references if needed (report schema, env vars)
- [x] Run quick_validate.py and fix issues
- [x] Add unit tests for non-network logic
- [x] Run tests

## 2026-03-17 - Agent System Settings Review

- [x] Compare local agent settings with `AGENTS_ANTIGRAVITY.md`
- [x] Save a checkpoint for sensitive system files
- [x] Update `AGENTS.md`
- [x] Update `.agents/skills/task-executor/SKILL.md`
- [x] Update `.agents/skills/safety-guardrails/SKILL.md`
- [x] Append dated sections to `research_notes.md`, `implementation_plan.md`, and `task.md`
- [x] Re-read changed files and log Tier 2 actions in `agent_audit.log`

## 2026-03-18 - Skill System Refactor

- [x] Review all local `SKILL.md` files for stale paths and duplicated workspace policy
- [x] Save a checkpoint for the affected system skill files
- [x] Create `.agents/skills/core-agent-rules/SKILL.md`
- [x] Update `AGENTS.md` to reference the shared policy skill
- [x] Refactor `task-executor`, `safety-guardrails`, and `skill-conductor` to reference `core-agent-rules`
- [x] Update `version-control` to remove obsolete tool references and tighten rollback rules
- [x] Validate the edited skills and write Tier 2 audit entries

## 2026-03-18 - Global Skill Mirror And Commit

- [x] Back up existing global system skills in `C:\Users\Admin\.agents\skills`
- [x] Add global `core-agent-rules`
- [x] Update global `task-executor`, `safety-guardrails`, and `skill-conductor`
- [x] Validate the updated global skills and confirm stale-pattern cleanup
- [x] Create a dedicated local git commit for the system-skill refactor

## 2026-03-18 - KB Vault Implementation

- [x] Create `workspace/` folder structure for the vault
- [x] Add `workspace/agents.md`
- [x] Add Markdown templates in `workspace/assets/`
- [x] Add minimal Markdown skills in `workspace/skills/`
- [x] Convert `kb_agent_instructions.docx` into `workspace/notes/kb-agent-instructions.md`
- [x] Add `workspace/notes/index.md` and `workspace/notes/setup-checklist.md`
- [x] Add starter project notes in `workspace/projects/`
- [x] Update root `AGENTS.md` for KB vault routing and Markdown-only rules
- [x] Verify the resulting vault structure and log the actions

## 2026-03-18 - NotebookLM MCP Auto Refresh

- [x] Confirm proxy-based NotebookLM access works with fresh browser tokens
- [x] Keep proxy settings in `C:\Users\Admin\.gemini\antigravity\mcp_config.json`
- [x] Save a checkpoint for NotebookLM workflow artifacts and scripts
- [x] Repair `notebooklm_auto_refresh.py`
- [x] Add `launch_notebooklm_debug_chrome.ps1`
- [x] Add `refresh_notebooklm_tokens.ps1`
- [x] Add `run_nlm_proxy.ps1`
- [x] Validate local syntax and helper outputs
- [x] Run one live refresh against Chrome DevTools
- [x] Re-run `nlm notebook get` for `254d43aa-a535-46f2-a65b-f6ce877256c9`
- [x] Re-run `nlm notebook get` for `21c4ad87-0b35-43ca-a31a-01ea3b648b17`

## 2026-03-18 - Cross-Update Stabilization

- [ ] Align root and vault rules on whether `.obsidian/` is an allowed exception inside `workspace/`
- [ ] Correct KB verification notes in `implementation_plan.md` and `task.md` so unresolved setup items are not marked as fully verified
- [ ] Refresh the `youtube-monitoring` sections in `research_notes.md` and `implementation_plan.md` to match Gemini/Anthropic support and current reference files
- [ ] Define local vs global skill source-of-truth policy for `.agents/skills/**` and `C:\Users\Admin\.agents\skills\`
- [ ] Make audit log writes newline-safe and document the logging rule
- [ ] Split the current dirty worktree into clear themed checkpoints before new feature work
- [ ] Only after the stabilization steps, continue with LLM fallback and monitoring-service integration
