# Tasks

- [x] Initialize skill scaffold in .agents/skills/youtube-monitoring
- [x] Copy skill.py, mcp_server.py, requirements.txt into scripts/
- [x] Draft SKILL.md with correct frontmatter and workflow instructions
- [x] Add references for provider env vars and runtime usage
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
- [x] Update root `AGENTS.md` for KB vault routing and Markdown-first rules with explicit Obsidian exceptions
- [x] Verify the initial vault structure and log the remaining operational setup items separately

## 2026-03-18 - Obsidian Productionization

- [x] Create checkpoint for vault productionization
- [x] Update instruction files to allow native `.base` files and real `.obsidian/plugins/**` exceptions
- [x] Configure vault settings in `.obsidian`
- [x] Add service/source/runbook templates and folders
- [x] Create service catalog and registry base files
- [x] Seed the vault with an initial real service record
- [x] Install and enable `terminal` and `obsidian-kanban`
- [x] Verify plugin state, base discovery, daily note configuration, and actual CLI command names

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
- [x] Re-verify `nlm notebook list` through `run_nlm_proxy.ps1`
- [x] Re-verify MCP `notebook_list` through the Python tool entrypoint with proxy env
- [x] Re-verify MCP `notebook_get` for both target notebook IDs
- [x] Fix external `mcp_config.json` entrypoint from `notebooklm_mcp.server` to `notebooklm_tools.mcp.server`

## 2026-03-18 - Cross-Update Stabilization

- [x] Align root and vault rules on whether `.obsidian/` is an allowed exception inside `workspace/`
- [x] Correct KB verification notes in `implementation_plan.md` and `task.md` so unresolved setup items are not marked as fully verified
- [x] Refresh the `youtube-monitoring` sections in `research_notes.md` and `implementation_plan.md` to match Gemini/Anthropic support and current reference files
- [x] Define local vs global skill source-of-truth policy for `.agents/skills/**` and `C:\Users\Admin\.agents\skills\`
- [x] Make audit log writes newline-safe and document the logging rule
- [x] Save a dedicated stabilization checkpoint for the current rules/artifacts cohort (`checkpoint_20260318_020141`)
- [x] Group the remaining unrelated dirty files into explicit commit/checkpoint themes before new feature work (`progress.md`, checkpoints `023712/023808/023809/023811/023813`)
- [ ] Only after the stabilization steps, continue with LLM fallback and monitoring-service integration

## 2026-03-18 - Budget Auto Components Radar Concept Review

- [x] Confirm the requested Markdown file exists and inspect its state
- [x] Recover the actual concept text from the adjacent `.rtf` source
- [x] Review the concept for product logic, delivery realism, and operational risks
- [x] Spot-check critical current-state assumptions against official documentation
- [x] Deliver a concise assessment with strengths, weaknesses, and recommended scope cuts

## 2026-03-18 - Budget Auto Components Radar Rewrite

- [x] Reuse the review findings as rewrite constraints
- [x] Draft a stronger management-facing Markdown structure
- [x] Add phased rollout steps with brief rationale per stage
- [x] Write the revised content into the requested external Markdown file
- [x] Verify the rewritten file is non-empty and readable

## 2026-03-18 - Dashboard And Service KB Expansion

- [x] Create a checkpoint for dashboard and service KB changes
- [x] Create a real Kanban board in `workspace/projects/`
- [x] Add a startup dashboard note for the vault
- [x] Seed the service catalog with real Obsidian operational services
- [x] Add supporting source and runbook notes for the seeded services
- [x] Repoint project navigation notes to the new main board and dashboard
- [x] Configure `workspace/.obsidian/workspace.json` for a dashboard-first startup layout
- [x] Verify the new board, notes, links, and CLI navigation

## 2026-03-18 - Cohort Staging Strategy (No Commit)

- [x] Confirm current index state and detect over-staged baseline
- [x] Add `scripts/git_cohort_stage.ps1` with dry-run and apply modes
- [x] Document exact baseline/staging/exclusion commands in `staging_strategy.md`
- [x] Keep commit action out of this step

## 2026-03-18 - Ecosystem Convergence Analysis

- [x] Audit current projects, chats, workflows, and topic groups from `My Dashboard`
- [x] Compare the dashboard inventory with the vault dashboard and architecture notes
- [x] Identify the main functional overlaps and non-overlaps
- [x] Write a permanent architecture analysis note in `workspace/notes/`
- [x] Define the canonical `project_id` registry across dashboard, vault, workflows, chats, and NotebookLM
- [x] Design the `project mode` launch contract for agent scenarios
- [x] Design the single inbox pipeline and write-back policy
- [x] Define the vault-to-dashboard export contract for generated `projects.json` and related summaries
- [x] Define the minimal YAML/frontmatter schema for `project`, `agent`, `idea`, `artifact`, `task`, and `report`
- [x] Design the weekly synthesis/report loop for changed projects

## 2026-03-18 - Dashboard Productization MVP

- [x] Extend `sync_workspace_data.py` to emit `data/project_registry.json`
- [x] Overlay dashboard export with canonical KB project/chat/workflow notes
- [x] Preserve existing KB entity notes unless explicit refresh is requested
- [x] Publish weekly brief into both dashboard docs and vault dashboards
- [x] Load project registry in `app.js` and merge launch-contract data into projects
- [x] Fix project modal task rendering to use canonical `keyTasks`
- [x] Add `Project mode`, KB open, and prompt copy actions in dashboard UI
- [x] Run syntax checks for Python and JavaScript
- [x] Run a real sync cycle and verify generated registry and weekly brief outputs

## 2026-03-18 - Legacy Chat Link Normalization

- [x] Measure current unlinked chat/workflow counts from generated dashboard state
- [x] Add evidence-based autolinking for legacy chat sessions
- [x] Add curated hint rules for NotebookLM, Dashboard, KB, grant, KORA, and monitoring chats
- [x] Sanitize `relatedProjectIds` against the canonical current project set
- [x] Reconcile links again after KB overlay and rebuild project chat/workflow counts
- [x] Re-run sync and verify unlinked chats dropped materially with zero invalid `project_id` references

## 2026-03-18 - External Audit Inventory

- [x] Define the full audit roots for the current system
- [x] Generate one flat UTF-8 inventory file with absolute paths
- [x] Generate a manifest with counts, sensitivity notes, and audit order
- [x] Verify both files are readable and the inventory count matches the collected scope
