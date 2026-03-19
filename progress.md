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
