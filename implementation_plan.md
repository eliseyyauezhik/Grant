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

## 2026-03-18 - Ecosystem Convergence Analysis

Objective
- Map the current overlap between `My Dashboard`, `Obsidian vault`, `NotebookLM`, chats, workflows, and agent projects, then define a pragmatic target architecture for convergence.

Execution steps
1. Inspect the generated dashboard data for projects, chats, workflows, and topic groupings.
2. Compare that inventory with the current vault dashboard, architecture note, and project summary.
3. Separate true duplication from valid layer specialization.
4. Define a recommended division of responsibility across UI, memory, agent execution, and external tool layers.
5. Capture the analysis in a permanent vault note that can guide future implementation work.

Verification
- Confirm the dashboard export still reflects the current project/chat/workflow counts.
- Confirm the vault note links back to the dashboard and target architecture notes.
- Confirm the resulting recommendation is consistent with the existing `My Dashboard -> Agent -> Vault` direction.

Extension from external `analysis_results.md`
6. Define the export contract from vault entities to dashboard JSON so dashboard becomes a generated UI layer instead of a parallel state store.
7. Define a minimal YAML/frontmatter schema for canonical entities (`project`, `agent`, `idea`, `artifact`, `task`, `report`).
8. Define a weekly synthesis/report loop that summarizes changed projects into vault reports for dashboard consumption.

## 2026-03-18 - Dashboard Productization MVP

Objective
- Ship a working MVP of the target architecture: vault-backed registry, dashboard `project mode`, and weekly synthesis export.

Execution steps
1. Finish the sync pipeline so it reads KB note overlays and emits a dedicated `project_registry.json`.
2. Preserve existing KB entity notes by default and refresh them only behind an explicit flag.
3. Publish weekly synthesis both into the dashboard workspace and into the vault dashboards layer.
4. Update `app.js` so the dashboard loads the registry, merges launch contracts into project cards, and exposes KB / prompt actions in the UI.
5. Validate syntax and run a real sync cycle to confirm generated artifacts and counts.

Verification
- `python -m py_compile C:\Users\Admin\.gemini\antigravity\scratch\Мой Дашборд\scripts\dashboard\sync_workspace_data.py`
- `node --check C:\Users\Admin\.gemini\antigravity\scratch\Мой Дашборд\app.js`
- `python C:\Users\Admin\.gemini\antigravity\scratch\Мой Дашборд\scripts\dashboard\sync_workspace_data.py`
- Verify `C:\Users\Admin\.gemini\antigravity\scratch\Мой Дашборд\data\project_registry.json` contains populated `launchContract` and `projectMode` data.
- Verify `C:\Users\Admin\.gemini\antigravity\scratch\Мой Дашборд\docs\weekly_project_brief.md` and `D:\ЯндексДиск\Yandex.Disk\ПРОЕКТЫ\KnowledgeBase\Dashboards\Weekly Project Brief.md` exist after sync.

## 2026-03-18 - Legacy Chat Link Normalization

Objective
- Normalize legacy chat-to-project links so the registry can support project-scoped execution and not only static viewing.

Execution steps
1. Measure current unlinked chat/workflow counts from generated dashboard state.
2. Add chat autolinking based on evidence text from title, summary, brain markdown snippets, and path hints.
3. Add curated domain hint rules for recurring system themes such as NotebookLM, Dashboard, Obsidian, grants, KORA, and monitoring.
4. Sanitize `relatedProjectIds` against the current canonical project set.
5. Run a second reconciliation pass after KB overlay and rebuild project chat/workflow counts from final entity links.

Verification
- `python -m py_compile C:\Users\Admin\.gemini\antigravity\scratch\Мой Дашборд\scripts\dashboard\sync_workspace_data.py`
- `python C:\Users\Admin\.gemini\antigravity\scratch\Мой Дашборд\scripts\dashboard\sync_workspace_data.py`
- Confirm `data/dashboard_data.json` drops unlinked chats from `21` to a materially smaller residual set and that invalid `project_id` references are gone.

## 2026-03-18 - External Audit Inventory

Objective
- Produce a complete absolute-path inventory of the current system so an external LLM can review the whole architecture, codebase, KB, session memory, and runtime config surface.

Execution steps
1. Define the audit roots that make up the real system.
2. Generate one flat UTF-8 inventory file with absolute paths only.
3. Generate a manifest that explains included roots, counts, sensitivity notes, and a recommended audit order.
4. Verify both files are readable and that the inventory line count matches the collected file count.

Verification
- Confirm the manifest exists and lists the included roots with counts.
- Confirm the inventory exists and contains one absolute path per line.
- Confirm the current total listed file count is `4772`.
- Confirm the curated bundle folder and ZIP exist and include redacted runtime files plus the external audit prompt.

## 2026-03-19 - Post-Audit Quick Wins

Objective
- Apply the first concrete corrections from the external audit instruction while preserving the current `Vault -> sync -> Dashboard` architecture.

Execution steps
1. Remove the `projects.json` input/output circular dependency by introducing `projects_manual_base.json` as the default manual source and keeping `projects.json` generated-only.
2. Seed the new manual base automatically from legacy generated data so the migration does not require a manual rename.
3. Fix project-notes duplication by deduplicating semicolon-separated note segments both during raw merge and during KB overlay.
4. Deduplicate workflows by normalized path before workflow IDs are created from CSV rows.
5. Gate NotebookLM via `NOTEBOOKLM_AVAILABLE` and publish `notebooklmEnabled` in registry contracts.
6. Add explicit AGENTS priority comments plus a root write-back protocol section to reduce policy ambiguity.
7. Re-run sync and assert the generated outputs match the new contract.

Verification
- `python -m py_compile C:\Users\Admin\.gemini\antigravity\scratch\Мой Дашборд\scripts\dashboard\sync_workspace_data.py`
- `python C:\Users\Admin\.gemini\antigravity\scratch\Мой Дашборд\scripts\dashboard\sync_workspace_data.py`
- Post-sync assertions on `projects_manual_base.json`, `project_registry.json`, `dashboard_data.json`, and the `tgaggregator` notes field.

Follow-up
- QW-6: add schema validation for project frontmatter before registry generation.
- QW-7: isolate `.obsidian/` from agent writable scope through explicit ignore/guardrail rules.

## 2026-03-28 - OpenClaw VPS Continuation

Objective
- Resume the existing OpenClaw VPS setup, verify the live gateway state, and install the official NVIDIA guardrails component in a way that does not overwrite the working OpenClaw deployment.

Execution steps
1. Connect to the VPS via SSH using the stored 4vps credentials and confirm the host identity.
2. Read `openclaw status` and the CLI help to determine the real current state of the gateway, Telegram channel, and daemon/install layout.
3. Check the NVIDIA note against official documentation and normalize the target to `NeMo Guardrails` rather than the non-official `NemoClaw` name.
4. Install the missing Ubuntu dependency `python3.10-venv`, create `/opt/nemoguardrails/venv`, and install `nemoguardrails` there.
5. Verify the package import/version inside the virtual environment and record whether any OpenClaw integration work is still needed.

Verification
- SSH command returns the live host name and OS version.
- `openclaw status` shows the actual service and channel state.
- `python -m pip show nemoguardrails` or an import/version check succeeds inside the dedicated venv.
- The workspace notes distinguish verified facts from the earlier hallucinated `NemoClaw` name.

## 2026-03-28 - NemoClaw Completion With OpenClaw Stop Allowed

Objective
- Complete NemoClaw onboarding on `4vps` by temporarily stopping the currently running OpenClaw gateway on port `18789`, with backup and rollback safety.

Execution steps
1. Re-read local constraints and parse VPS credentials from local secure notes without exposing secrets in logs/chat.
2. Connect to VPS and verify current OpenClaw/NemoClaw state plus exact port listeners.
3. Create host-side backup archives of `/root/.openclaw` and `/root/.nemoclaw`.
4. Stop host OpenClaw gateway process/service and verify port `18789` is free.
5. Run `nemoclaw onboard --non-interactive` with explicit Anthropic provider env and capture logs.
6. Verify NemoClaw sandbox status and OpenShell forwarding on `18789`.
7. Record outcome and exact rollback command set if onboarding fails.

Verification
- Backup archives exist in `/root/nemoclaw-backups`.
- `ss -ltnp` no longer shows host OpenClaw listener before onboarding.
- Onboarding exits successfully (`exit code 0`) and `nemoclaw list/status` reports healthy state.
- If onboarding fails, logs are saved and rollback instructions are validated against current process state.

Execution update
- Backups were created successfully in `/root/nemoclaw-backups`.
- `OpenClaw` did not need to be stopped by this run because the gateway service was already inactive and port `18789` was free.
- `nemoclaw onboard --resume --non-interactive` was executed and progressed past image build, but failed again during `openshell sandbox create`.
- Verified root cause from kernel logs: the VPS hit global OOM and the `openshell` process was killed while exporting the sandbox into the gateway.
- Rollback was validated by restarting `OpenClaw` with `openclaw gateway start`; the gateway is reachable again on `127.0.0.1:18789`.
- Remaining prerequisite before any further retry: add swap and/or move the VPS to a higher-RAM plan.

## 2026-03-28 - NemoClaw Retry After Swap And Disk Recovery

Objective
- Remove the remaining solvable VPS resource blockers, retry `NemoClaw` once more with rollback safety, and stop only when the real limiting factor of the current plan is proven.

Execution steps
1. Confirm the current live VPS state and restore `OpenClaw` first if it is down.
2. Identify the heaviest host and gateway disk consumers instead of assuming Docker-image totals are the full picture.
3. Remove only clearly disposable `NemoClaw` artifacts:
   - abandoned temp tarballs
   - old unused `openshell/sandbox-from:*` images
   - dangling image layers
4. Re-run `nemoclaw onboard --resume --non-interactive` with the existing Anthropic credential source injected from the already configured OpenClaw auth profile.
5. If the retry still fails, restore `OpenClaw`, clean failed `NemoClaw` runtime artifacts, and record the exact final blocker.

Verification
- `OpenClaw` is reachable again on `127.0.0.1:18789` after the retry.
- `openclaw status` shows Telegram `ON / OK`.
- Host root free space is restored to a non-critical level after cleanup.
- Notes clearly distinguish solved blockers from the remaining hard limit.

Execution update
- `OpenClaw` was found stopped at the beginning of this pass and was restored before deeper disk analysis.
- Swap remained active and healthy (`2.0 GiB`), confirming that memory was no longer the live blocker.
- Cleanup before the retry freed space by removing:
  - stale `/tmp/openshell-images.tar` in the failed gateway
  - old `openshell/sandbox-from:*` images and dangling layers
- The next retry progressed further than any previous run:
  - healthy gateway recreation
  - successful inference configuration
  - successful sandbox image build
  - successful image upload into the gateway
- The retry still failed in `sandbox`, but only after the gateway upload completed.
- At the failure point the root filesystem hit `100%` usage, after which the run ended with `tls handshake eof`.
- Post-failure stabilization removed the failed `openshell-cluster-nemoclaw` container and its Docker volume, restoring about `3.9G` free on `/`.
- Final state is stable again: `OpenClaw` restored, Telegram healthy, `NemoClaw` not onboarded.

## 2026-03-28 - OpenClaw Security Hardening

Objective
- Freeze the project on `OpenClaw` only, convert the live VPS deployment to a safer single-owner baseline, and capture the exact state in a dossier for external review.

Execution steps
1. Re-check the live `OpenClaw` status, security audit, sandbox explain output, and current `openclaw.json`.
2. Cross-check local best-practice notes against official OpenClaw security/config docs and keep only settings that are validated for `2026.3.24`.
3. Back up the live config on the VPS and apply the hardening changes:
   - sandbox `all`
   - messaging profile
   - deny runtime/fs/ui/nodes/automation surfaces
   - disable elevated host execution
   - disable Telegram groups
   - tighten file permissions
4. Re-run `openclaw config validate`, `openclaw status`, `openclaw security audit --json`, and `openclaw doctor`.
5. Clean any config artifacts created during CLI-based updates and verify the final JSON structure.
6. Record the final operating model and instructions in project artifacts plus a standalone external-review dossier.

Verification
- `openclaw status` shows the gateway reachable on `127.0.0.1:18789`.
- Telegram remains `ON / OK`.
- `openclaw security audit --json` falls to one residual warning only.
- `/root/.openclaw` and key config/auth files use tightened permissions.
- A standalone Markdown dossier exists with the sanitized final config and operating instructions.

## 2026-03-30 - Telegram Chat Analysis Prompt Pack Run

Objective
- Execute the staged prompt-pack on the Telegram export and save Stage 1 / Stage 2 / Final analysis outputs plus a short human-readable recap.

Target files
- `workspace/projects/telegram-chat-analysis-prompt-pack/runs/2026-03-29_openclaw-lab-community/stage1_claims.json`
- `workspace/projects/telegram-chat-analysis-prompt-pack/runs/2026-03-29_openclaw-lab-community/stage2_topics.json`
- `workspace/projects/telegram-chat-analysis-prompt-pack/runs/2026-03-29_openclaw-lab-community/final_analysis.json`
- `workspace/projects/telegram-chat-analysis-prompt-pack/runs/2026-03-29_openclaw-lab-community/analysis_summary.md`
- `.agents/handovers/handover_2026-03-29_telegram-chat-analysis.md`
- workflow artifacts and audit trail

Plan
1. Read the prompt-pack, schemas, owner profile, backlog, and Telegram export structure — risk: LOW
2. Extract dataset facts and identify the highest-signal message clusters before claiming anything — risk: LOW
3. Build Stage 1 claims with message refs, chronology, and uncertainty markers — risk: MEDIUM
4. Consolidate into Stage 2 topics and produce the final analysis/tuning brief — risk: MEDIUM
5. Validate JSON syntax, then write back to artifacts and handover — risk: LOW

Verification
- Load all three JSON outputs with Python `json.load`
- Confirm the output folder contains all expected artifacts
- Re-read the final analysis summary for coherence with the saved JSON files

## 2026-03-28 - OpenClaw Cost Switch to Haiku and In-Bot Model Picker

Goal
- Lower Telegram operating cost by moving the default OpenClaw model from Sonnet to Haiku, while keeping an easy owner-side way to switch models directly from the bot.

Plan
1. Confirm the live model policy, allowlist, and active Telegram owner sessions — risk: LOW.
2. Cross-check the current OpenClaw model schema and `/model` command behavior against official docs — risk: LOW.
3. Back up the live config and switch the documented primary/fallback policy to Haiku + Sonnet — risk: MEDIUM.
4. Expand the model allowlist with aliases so `/model haiku` and `/model sonnet` are available — risk: MEDIUM.
5. Reset only the owner Telegram direct/slash session mappings, restart the gateway through the official CLI path, and verify health — risk: MEDIUM.
6. Re-publish the Telegram command menu with `/model`, then send a completion notice into the owner chat — risk: MEDIUM.

Verification
- `openclaw config validate` passes.
- `openclaw models status --plain` resolves to `anthropic/claude-haiku-4-5-20251001`.
- `openclaw status --deep` shows gateway reachable and Telegram `ON / OK`.
- `getMyCommands` for the owner chat includes `/model`.
- `sessions.json` no longer contains the old owner direct/slash session mappings.

Execution result
- All six steps completed successfully.
- One initial config attempt was rolled back automatically after validation because the wrong key `fallback` was used instead of the current documented `fallbacks`.
- A first restart attempt via `systemctl restart openclaw` failed because the actual managed unit is `openclaw-gateway.service`; the final restart was completed successfully through `openclaw gateway restart`.

## 2026-03-28 - OpenClaw Bot Menu and Audio Cleanup

Goal
- Continue the latest OpenClaw VPS handover by fixing the stale Telegram command menu and migrating the legacy audio config to the current documented layout without breaking the live bot.

Plan
1. Re-check the real live state of the gateway, Telegram channel, and slash-command menu — risk: LOW.
2. Compare the live audio config with the current OpenClaw documentation and confirm the real root cause of the warning — risk: LOW.
3. Create a reversible backup of `/root/.openclaw/openclaw.json` and migrate the legacy audio entry to `tools.media.audio` — risk: MEDIUM.
4. Validate the config and perform a safe background restart with a health-check loop and rollback path — risk: MEDIUM.
5. Replace the Telegram bot menu with a compact Russian set of only currently supported slash commands — risk: MEDIUM.

Verification
- `openclaw config validate` passes after the edit.
- `openclaw status` shows the gateway reachable on `127.0.0.1:18789` and Telegram `ON / OK` after restart.
- The stale `plugins.entries.audio` warning disappears from status output.
- `getMyCommands` returns only the intended compact command set.

Execution result
- All five steps completed successfully.
- The final supported Telegram menu was intentionally limited to `new`, `status`, `reset`, `help`, and `stop`; `/resume` was not published because the current OpenClaw build does not expose it as a supported slash command.

## 2026-03-28 - OpenClaw KB Awareness and Owner Menu Upgrade

Goal
- Correct the bot's self-understanding about the mounted Obsidian vault, restore the persistent Telegram menu, add an owner-friendly restart command, and run a compact architecture/health pass.

Plan
1. Inspect the remote workspace bootstrap/identity files and confirm whether they still describe a generic first-run bot — risk: LOW.
2. Verify the real state of `KnowledgeBase/`, `rclone-kb.service`, and Telegram menu/button settings — risk: LOW.
3. Update workspace source-of-truth files so fresh sessions know about the mounted Obsidian vault and answer access questions precisely — risk: MEDIUM.
4. Clear the stale Telegram direct-session mapping so the next real DM starts from the corrected workspace context — risk: MEDIUM.
5. Reconfigure Telegram commands/menu:
   - default/private compact Russian menu
   - owner-specific Russian menu with `/restart`
   - force menu button to `commands`
   — risk: MEDIUM.
6. Re-enable `commands.restart`, then re-run health checks and smoke-test a fresh non-delivered session for vault-access truthfulness — risk: MEDIUM.
7. Clean obvious post-fix operational noise (`memorySearch` without provider, orphan session files) and re-run doctor — risk: MEDIUM.

Verification
- `getChatMenuButton` returns `commands` for the owner chat.
- `getMyCommands` returns the intended owner command set in Russian.
- Fresh smoke session states that mounted `KnowledgeBase/` is accessible.
- `openclaw status --deep` shows Telegram `ON / OK`.
- `openclaw security audit --json` remains free of critical findings.
- `openclaw doctor` no longer reports orphan session files and reports memory search disabled.

Execution result
- All seven steps completed successfully.
- Telegram native grouping still does not exist, so grouping was approximated through ordered commands and category-style Russian descriptions.

## 2026-03-28 - OpenClaw Security Hardening

Objective
- Freeze the project on `OpenClaw` only, convert the live VPS deployment to a safer single-owner baseline, and capture the exact state in a dossier for external review.

Execution steps
1. Re-check the live `OpenClaw` status, security audit, sandbox explain output, and current `openclaw.json`.
2. Cross-check local best-practice notes against official OpenClaw security/config docs and keep only settings that are validated for `2026.3.24`.
3. Back up the live config on the VPS and apply the hardening changes:
   - sandbox `all`
   - messaging profile
   - deny runtime/fs/ui/nodes/automation surfaces
   - disable elevated host execution
   - disable Telegram groups
   - tighten file permissions
4. Re-run `openclaw config validate`, `openclaw status`, `openclaw security audit --json`, and `openclaw doctor`.
5. Clean any config artifacts created during CLI-based updates and verify the final JSON structure.
6. Record the final operating model and instructions in project artifacts plus a standalone external-review dossier.

Verification
- `openclaw status` shows the gateway reachable on `127.0.0.1:18789`.
- Telegram remains `ON / OK`.
- `openclaw security audit --json` falls to one residual warning only.
- `/root/.openclaw` and key config/auth files use tightened permissions.
- A standalone Markdown dossier exists with the sanitized final config and operating instructions.
## 2026-03-30 - Verified Corpus-to-Roadmap Skill

Goal
- Turn the existing Telegram analysis into a reusable pipeline that verifies claims, sorts them into three confidence baskets, scores them for practical value, ranks them for `OpenClaw` and project use, and packages the workflow as a local skill.

Scope
- Current analysis artifacts under `workspace/projects/telegram-chat-analysis-prompt-pack/runs/2026-03-29_openclaw-lab-community/`
- The prompt-pack in `workspace/projects/telegram-chat-analysis-prompt-pack/`
- Shared workflow artifacts: `research_notes.md`, `implementation_plan.md`, `task.md`, `progress.md`
- New or updated files under `.agents/skills/**` after confirmation

Constraints
- Use official sources first for verification.
- Keep the workflow reusable for other chat/database corpora, not only this `OpenClaw` case.
- Separate stable corpus-processing logic from broader user-specific "life orchestration" ambitions.
- Keep model/subagent routing explicit and optimization-oriented.

Success
- A clear `3-basket` evidence model is defined.
- A prioritization rubric exists for confidence, applicability, impact, volatility, and implementation cost.
- The current `OpenClaw` corpus is re-ranked with that rubric.
- A concrete plan of application/implementation is produced from the ranked knowledge.
- A validated local skill exists that can reproduce the pipeline on another corpus.

Plan
1. Define the verification ledger and the `3-basket` evidence model (`verified`, `probable but unverified`, `obsolete/noisy/contradicted`) - risk: LOW
2. Define the prioritization rubric and weighting logic for project relevance and `OpenClaw` operational value - risk: MEDIUM
3. Apply the rubric to the current `OpenClaw` corpus and produce a ranked rollout roadmap - risk: MEDIUM
4. Design the reusable skill contract:
   - use cases
   - trigger phrases
   - negative triggers
   - model/subagent routing decision tree
   - required outputs
   risk: MEDIUM
5. Create a checkpoint and scaffold the new skill under `.agents/skills/` with `SKILL.md` plus `references/` and `scripts/` if justified - risk: HIGH -> needs confirmation
6. Validate the skill structure and run an evaluation pass on the current `OpenClaw` corpus as the baseline case - risk: MEDIUM

Verification
- Re-read the basket rules and scoring rubric for ambiguity.
- Check that the ranked items clearly map to actions, not only themes.
- Validate the skill via `quick_validate.py` and, if useful, `eval_skill.py`.
- Confirm the skill does not over-trigger on ordinary summarization requests.
Execution notes
- Keep the sequence strict:
  1. official-source verification
  2. evidence buckets
  3. ranking
  4. human-readable roadmap
  5. reusable skill packaging
- Deliver the current corpus in a readable form, not only as JSON:
  - a reusable framework doc
  - a run-specific verified knowledge library + roadmap
- Package the workflow as a narrow reusable skill:
  - `verified-corpus-roadmap`
  - scope limited to corpus -> verification -> triage -> prioritization -> roadmap
  - no broad orchestration/life-help wrapper in v1
- Keep user-facing outputs in Russian:
  - basket labels
  - comments
  - roadmap interpretations
- Use the current corpus workflow as the seed of the wider `Analytical Node`, not as an isolated Telegram-only artifact.
