# Implementation Plan

Skill name
- youtube-monitoring (kebab-case, <=64 chars)

Stack
- Python
- yt-dlp
- Gemini API (`gemini-2.5-pro` by default) or Anthropic API (`claude-opus-4-6`)
- MCP-compatible HTTP server (BaseHTTPRequestHandler)

Target structure
- .agents/skills/youtube-monitoring/SKILL.md
- .agents/skills/youtube-monitoring/scripts/skill.py
- .agents/skills/youtube-monitoring/scripts/mcp_server.py
- .agents/skills/youtube-monitoring/scripts/requirements.txt
- .agents/skills/youtube-monitoring/references/reference.md
- .agents/skills/youtube-monitoring/tests/test_core.py

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
4. Add minimal references for provider env vars and runtime usage
5. Run quick_validate.py for the new skill
6. Add and run unit tests for non-network logic

Notes
- Keep SKILL.md concise and imperative
- Include triggers and negative triggers in description
- Default provider is Gemini unless `LLM_PROVIDER` overrides it
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
2. Add `workspace/agents.md` with Markdown-first, graph-first, and template-first rules plus explicit Obsidian exceptions.
3. Add minimal templates and Markdown skills for kanban, capture, and review workflows.
4. Convert `kb_agent_instructions.docx` into a Markdown note inside `workspace/notes/` and derive a setup checklist from it.
5. Add starter notes for navigation and task intake.
6. Update the root `AGENTS.md` so KB work is explicitly routed to `workspace/`.
7. Verify that `workspace/` contains Markdown-first KB content plus allowed `.base` views and `workspace/.obsidian/*.json`, and that the main notes reference the new skills and templates.

Verification targets
- `workspace/notes/index.md` links to rules, skills, templates, and active project notes.
- `workspace/` uses Markdown-first storage with only the documented native Obsidian exceptions: `.base` and `workspace/.obsidian/*.json`.
- Root and vault-specific instructions agree on `workspace/` boundaries, allowed Obsidian-native files, and `_assets_bin/`.
- Remaining operational Obsidian setup checks stay tracked in `workspace/notes/setup-checklist.md` and are not implied complete by the initial structure verification.

## 2026-03-18 - Obsidian Productionization

Objective
- Configure the vault as an operational knowledge system for service records, source references, and agent-friendly daily work.

Execution steps
1. Update instruction files to allow official Obsidian `.base` files in `workspace/` and service JSON in `workspace/.obsidian/`.
2. Configure `.obsidian/app.json`, `.obsidian/templates.json`, and `.obsidian/daily-notes.json` for controlled capture, links, templates, and attachments.
3. Add KB folders and templates for services, sources, runbooks, decisions, inbox items, and daily operations.
4. Create `.base` views for service catalog, source registry, and runbooks.
5. Seed the vault with one real service record and supporting source/runbook notes so the database is not empty.
6. Install minimal community plugins that directly support the intended workflow: `terminal` and `obsidian-kanban`.
7. Verify CLI commands, plugin state, and base discovery through Obsidian CLI.

Verification
- `obsidian vault=workspace plugins:enabled` includes the intended core/community plugins.
- `obsidian vault=workspace bases` lists the new `.base` files.
- `obsidian vault=workspace base:views ...` resolves the expected views.
- `obsidian vault=workspace daily:path` resolves into the configured daily folder pattern.

Execution update
- Root and vault rules were aligned with the actual CLI surface: `links` / `backlinks` are available, while `link-path` / `backlink-path` are not.
- The vault policy was widened to reflect the real production state of `.obsidian/plugins/**`, because installed community plugins store `*.json`, `*.js`, and `*.css` there.
- Community plugins `terminal` and `obsidian-kanban` were installed from the official registry/GitHub release assets and enabled successfully.
- Verified runtime commands:
  - `Obsidian.com vault=workspace plugins:enabled filter=community versions format=json`
  - `Obsidian.com vault=workspace bases`
  - `Obsidian.com vault=workspace open path=projects/services.base` then `Obsidian.com vault=workspace base:views`
  - `Obsidian.com vault=workspace daily:path`

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

## 2026-03-18 - Budget Auto Components Radar Concept Review

Objective
- Evaluate the feasibility and business quality of the local "budget market radar" concept for Russian auto components production and development monitoring.

Plan
1. Confirm the requested file exists and inspect its real contents or placeholders.
2. Recover the concept text from the nearest authoritative local source if the target file is empty.
3. Assess strengths, delivery realism, data risks, and missing validation logic.
4. Spot-check a few critical external assumptions from official documentation where current-state accuracy matters.
5. Report a concise verdict with concrete improvements to the concept.

Verification
- Confirm the target `.md` file state on disk.
- Extract readable text from the `.rtf` source and review the full concept body.
- Verify at least the messaging and open-data assumptions against current official documentation where easily accessible.

## 2026-03-18 - Budget Auto Components Radar Rewrite

Objective
- Turn the reviewed concept into a stronger Markdown document that management can read as a realistic MVP proposal rather than as a broad AI vision note.

Plan
1. Reuse the review findings as rewrite constraints: cut overclaims, make the scoring model explicit, and narrow MVP scope.
2. Draft a new structure focused on management value, MVP boundaries, sources, scoring, architecture, metrics, risks, and decision framing.
3. Add a phased rollout where each stage has a short rationale for why it appears in that order.
4. Write the revised content into the requested external Markdown file.
5. Verify file size, encoding, and top-of-file readability after the write.

Verification
- Confirm the external `.md` file is no longer 0 bytes.
- Read the first section back from disk to verify UTF-8 Markdown output.
- Confirm the rewritten document contains the planned sections and stage rationales.

## 2026-03-18 - Dashboard And Service KB Expansion

Objective
- Implement all three remaining Obsidian workflow upgrades: a real kanban board, seeded service records for the Obsidian operating stack, and a startup dashboard layout for the vault.

Execution steps
1. Create a safe checkpoint for the notes, project files, and workspace layout that will be edited.
2. Create `projects/ops-board.md` through the installed Kanban plugin and seed it with actionable columns/cards.
3. Add `notes/dashboard.md` as the landing page for the vault.
4. Seed the service database with concrete operational records and matching source/runbook notes.
5. Update `notes/index.md`, `projects/README.md`, `task-inbox.md`, `service-catalog.md`, and `source-registry.md` so the new operating model is discoverable.
6. Replace `workspace/.obsidian/workspace.json` with a startup layout focused on dashboard + services base + ops board.
7. Reload the vault and verify the new notes, links, service counts, and CLI-driven navigation.

Verification
- `projects/ops-board.md` exists and contains Kanban frontmatter plus seeded lists.
- `notes/services/` contains multiple real service records tied to source and runbook notes.
- `notes/dashboard.md` exists and links to the main board and registries.
- `workspace/.obsidian/workspace.json` points at the new dashboard-centric layout.

## 2026-03-18 - Dirty Worktree Grouping

Objective
- Split the current dirty worktree into rollback-safe thematic cohorts before new feature work.

Cohorts and checkpoints
1. Governance and stabilization -> `checkpoint_20260318_023712`
2. YouTube monitoring skill source -> `checkpoint_20260318_023808`
3. NotebookLM helper scripts -> `checkpoint_20260318_023809`
4. Workspace vault -> `checkpoint_20260318_023811`
5. Site and reference outputs -> `checkpoint_20260318_023813`
6. Local generated artifacts -> no checkpoint required, exclude from commit planning by default

Verification
- Each commit candidate cohort has a dedicated clean checkpoint ID.
- `progress.md` records the mapping and the recommended commit order.
- `checkpoint_20260318_023731` is explicitly marked as mixed and should not be used for rollback.

## 2026-03-18 - Cohort Staging Strategy (No Commit)

Objective
- Prepare an executable, low-risk staging workflow for the current dirty worktree without creating commits.

Execution steps
1. Capture the current index risk: most files are already staged and include generated artifacts.
2. Add a reusable cohort staging script with dry-run mode and optional apply mode.
3. Define a deterministic baseline sequence (`git restore --staged .`) before cohort staging.
4. Document exact staging commands and generated-artifact exclusions in a dedicated strategy note.
5. Keep commit execution out of scope for this step.

Verification
- `scripts/git_cohort_stage.ps1` supports `show`, single-cohort staging, `all`, `-ResetIndexFirst`, `-ExcludeGenerated`, and `-ShowStatus`.
- `staging_strategy.md` contains baseline, dry-run, apply, exclusion, and validation commands.
- Existing checkpoint mapping remains aligned with `progress.md`.
