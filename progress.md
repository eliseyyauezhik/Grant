# Progress

## 2026-03-18 - Dirty Worktree Cohorts

Clean checkpoint cohorts
- `governance_stabilization` -> `checkpoint_20260318_023712`
  Files: `AGENTS.md`, `.agents/skills/safety-guardrails/SKILL.md`, `research_notes.md`, `implementation_plan.md`, `task.md`, `agent_audit.log`
  Intent: repo rules, workflow artifacts, audit hygiene.
- `youtube_monitoring_skill` -> `checkpoint_20260318_023808`
  Files: `.agents/skills/youtube-monitoring/` source files only.
  Intent: commit candidate for the local YouTube monitoring skill.
- `notebooklm_helpers` -> `checkpoint_20260318_023809`
  Files: `launch_notebooklm_debug_chrome.ps1`, `notebooklm_auto_refresh.py`, `refresh_notebooklm_tokens.ps1`, `run_nlm_proxy.ps1`.
  Intent: commit candidate for local NotebookLM auth/proxy tooling.
- `workspace_vault` -> `checkpoint_20260318_023811`
  Files: full `workspace/` tree including `.obsidian`, templates, notes, bases, and skills.
  Intent: commit candidate for the KB vault and dashboard/service expansion.
- `site_and_reference_outputs` -> `checkpoint_20260318_023813`
  Files: `index_v3.html`, `PROJECT_LINKS.md`, `_bases_syntax.html`, `_obsidian_cli_help.html`, transcripts, and optimized media outputs.
  Intent: separate review bucket for site/export/reference outputs.

Non-commit local artifact cohort
- `.agents/checkpoints/**`
- `__pycache__/`
- `.agents/skills/youtube-monitoring/scripts/__pycache__/`
- `.agents/skills/youtube-monitoring/tests/__pycache__/`
- `.agents/skills/youtube-monitoring/scripts/logs/*.log`
- `.agents/skills/youtube-monitoring/tests/tmp_kb/knowledge_base.json`
Reason: generated or operational artifacts; keep local unless a later task explicitly asks to version them.

Checkpoint warning
- `checkpoint_20260318_023731` is contaminated by a same-second ID collision between the first YouTube and NotebookLM checkpoint attempts. Do not use it for rollback decisions.

Suggested commit order
1. `governance_stabilization`
2. `youtube_monitoring_skill`
3. `notebooklm_helpers`
4. `workspace_vault`
5. `site_and_reference_outputs`

## 2026-03-18 - Staging Automation

- Added script: `scripts/git_cohort_stage.ps1`
- Added runbook: `staging_strategy.md`
- Script defaults to dry-run and supports:
  - `-Cohort governance|youtube|notebooklm|workspace|site|all`
  - `-ResetIndexFirst`
  - `-ExcludeGenerated`
  - `-ShowStatus`
  - `-Apply` for actual staging operations

## 2026-03-18 - Dashboard Productization MVP

- Dashboard workspace now has a generated canonical registry at `C:\Users\Admin\.gemini\antigravity\scratch\Мой Дашборд\data\project_registry.json`.
- `sync_workspace_data.py` now overlays dashboard exports with KB notes, preserves existing entity notes by default, and emits weekly briefs into both the dashboard docs and the vault dashboards layer.
- `C:\Users\Admin\.gemini\antigravity\scratch\Мой Дашборд\app.js` now exposes a registry-backed `Project mode` with KB/open and prompt-copy actions.
- Validation completed with:
  - `python -m py_compile C:\Users\Admin\.gemini\antigravity\scratch\Мой Дашборд\scripts\dashboard\sync_workspace_data.py`
  - `node --check C:\Users\Admin\.gemini\antigravity\scratch\Мой Дашборд\app.js`
  - `python C:\Users\Admin\.gemini\antigravity\scratch\Мой Дашборд\scripts\dashboard\sync_workspace_data.py`
- Current MVP blocker removed: the dashboard is no longer only a static view over `projects.json`; it now has a working launch contract layer for project-scoped agent work.

## 2026-03-18 - Legacy Chat Link Normalization

- Added evidence-based chat autolinking in `C:\Users\Admin\.gemini\antigravity\scratch\Мой Дашборд\scripts\dashboard\sync_workspace_data.py`.
- Added a post-overlay reconciliation pass so KB-derived links and legacy CSV/brain evidence converge before export.
- Current measured result after sync:
  - unlinked chats: `21 -> 4`
  - unlinked workflows: `0`
  - invalid chat `project_id` references: `3 -> 0`
- Remaining ambiguous legacy chats for optional manual curation:
  - `Task Plan`
  - `Текущие задачи`
  - `Поиск фотографий`
  - `Agent Second Brain Task Plan`

## 2026-03-18 - External Audit Inventory

- Added full-system audit artifacts:
  - `system_audit_full_file_inventory_2026-03-18_23-32-39.txt`
  - `system_audit_manifest_2026-03-18_23-32-39.md`
- Added curated upload-ready audit package:
  - `external_audit_bundle_2026-03-18_23-45-29/`
  - `external_audit_bundle_2026-03-18_23-45-29.zip`
- Included roots:
  - current repository
  - scratch dashboard workspace
  - KnowledgeBase vault
  - Antigravity brain/session store
- `mcp_config.json`
- NotebookLM runtime/profile cache
- Current inventory size: `4772` absolute file paths.
- Current curated bundle size: `48` copied/redacted source files plus prompt/meta files.

## 2026-03-19 - Post-Audit Quick Wins

- Manual backup of target files saved to `.agents/checkpoints/manual_post_audit_qw_20260319_000732`.
- Dashboard sync now reads manual overrides from `C:\Users\Admin\.gemini\antigravity\scratch\Мой Дашборд\projects_manual_base.json` and keeps `C:\Users\Admin\.gemini\antigravity\scratch\Мой Дашборд\projects.json` as generated output only.
- `C:\Users\Admin\.gemini\antigravity\scratch\Мой Дашборд\scripts\dashboard\sync_workspace_data.py` now:
  - seeds `projects_manual_base.json` automatically on first run;
  - deduplicates project notes by `;` segments, including KB overlay;
  - skips duplicate workflow rows by normalized path;
  - publishes `notebooklmEnabled=false` and excludes `notebooklm` from `allowedTools` unless `NOTEBOOKLM_AVAILABLE=true`.
- Root, KB, and dashboard instruction files now carry an explicit AGENTS precedence marker, and root `AGENTS.md` contains a dedicated write-back protocol section.
- Verification passed after live sync:
  - `projects_manual_base.json` created automatically;
  - `tgaggregator.notes` reduced to one unique note segment;
  - generated workflows remain unique by normalized path;
  - all launch contracts default to `notebooklmEnabled=false`.
