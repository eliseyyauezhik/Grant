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

## 2026-03-28 - OpenClaw VPS Continuation

- Verified the live VPS by SSH and confirmed the host is `Ubuntu 22.04.5 LTS`.
- Confirmed `OpenClaw 2026.3.24 (cff6dc9)` is installed and the gateway service is active.
- Confirmed Telegram is ON, while the separate node service is not installed.
- Installed `python3.10-venv` and the official NVIDIA `nemoguardrails 0.21.0` package in `/opt/nemoguardrails/venv`.
- Normalized the earlier `NemoClaw` wording to the official `NeMo Guardrails` name.
- Next decision: wire the guardrails layer into OpenClaw or leave it as a separate runtime for later integration.

## 2026-03-28 - NemoClaw Retry And Rollback

- Confirmed the earlier port blocker was cleared: `OpenClaw` was already stopped and `18789` was free before retrying `NemoClaw`.
- Added fresh rollback archives on the VPS:
  - `/root/nemoclaw-backups/openclaw_pre_resume_20260328_003059.tgz`
  - `/root/nemoclaw-backups/nemoclaw_pre_resume_20260328_003059.tgz`
- Resumed `nemoclaw onboard --non-interactive` successfully through inference and sandbox image build.
- Verified the sandbox image was rebuilt as `openshell/sandbox-from:1774654357`.
- Confirmed the second sandbox failure is caused by host memory exhaustion, not by a remaining port issue.
- Verified kernel OOM records for the killed `openshell` process while `openshell sandbox create` was pushing the image into the gateway.
- Restored the working `OpenClaw` gateway with `openclaw gateway start`.
- Final live state after rollback:
  - `openclaw-gateway.service` running
  - `127.0.0.1:18789` listening again
  - Telegram channel `ON / OK`
- Next required change before another `NemoClaw` retry: add swap and/or increase VPS RAM.

## 2026-03-28 - NemoClaw Final Retry And VPS Stabilization

- Enabled persistent swap earlier in the same operating thread and confirmed it remained active during the later retries.
- Restored `OpenClaw` when it was found down before the final diagnostic/cleanup pass.
- Identified real disk consumers beyond the simple Docker-image summary:
  - abandoned `openshell-images.tar` in the failed gateway
  - failed `NemoClaw` image layers
  - later, a large failed `openshell-cluster-nemoclaw` Docker volume
- Performed targeted cleanup before the final retry:
  - removed stale temp tar from the failed gateway
  - removed old unused `openshell/sandbox-from:*` images and dangling layers
- Confirmed a separate credential blocker and solved it without asking the user for a new secret:
  - `nemoclaw onboard` did not inherit `ANTHROPIC_API_KEY` from the shell
  - the already configured OpenClaw auth profile contained the required Anthropic API key source
- Final retry progression:
  - gateway recreated and became healthy
  - inference provider configured successfully
  - sandbox image built successfully
  - image upload into the gateway completed successfully
- Final retry still failed at `sandbox`, but only after crossing all earlier blockers.
- New terminal failure signature:
  - root filesystem dropped to `35M` free and then effectively `0`
  - onboarding ended with `tls handshake eof`
- Stabilization after the failed run:
  - removed failed `openshell-cluster-nemoclaw` container
  - removed failed `openshell-cluster-nemoclaw` volume
  - free disk recovered to about `3.9G`
  - restored `OpenClaw` and verified:
    - gateway reachable on `127.0.0.1:18789`
    - Telegram `ON / OK`
- Current proven conclusion:
  - `NemoClaw` is no longer blocked by port conflict, RAM, or missing shell env
  - the remaining blocker is disk capacity of the current VPS plan during final sandbox creation

## 2026-03-28 - OpenClaw Security Hardening

- The project was intentionally frozen on `OpenClaw` only; `NemoClaw` is deferred until the VPS plan changes.
- The live `OpenClaw` deployment on `4vps` was hardened to a much narrower single-owner baseline:
  - `sandbox.mode = all`
  - `sandbox.workspaceAccess = none`
  - `tools.profile = messaging`
  - runtime/filesystem/UI/nodes/automation surfaces denied
  - `tools.elevated.enabled = false`
  - Telegram groups disabled
- Host-side file permissions were tightened:
  - `/root/.openclaw` -> `700`
  - config/auth files -> `600`
- Final verified live state:
  - gateway reachable on `127.0.0.1:18789`
  - Telegram `ON / OK`
  - `openclaw security audit --json` -> `0 critical / 1 warn / 1 info`
- Remaining non-blocking notes:
  - only residual audit warning: `gateway.trusted_proxies_missing`
  - sandbox base image is still absent, but current denied tool surface makes that non-blocking
  - memory search is now explicitly disabled until a real embedding-provider decision is made
- New documentation artifacts created for continuation and external review:
  - `.agents/handovers/handover_2026-03-28_openclaw-security-hardening.md`
  - `openclaw_project_dossier_2026-03-28.md`

## 2026-03-28 - OpenClaw Cost Switch to Haiku and In-Bot Model Picker

- Verified from the live VPS and official docs that the current OpenClaw schema uses `agents.defaults.model.fallbacks`, not `fallback`.
- Switched the default model from `anthropic/claude-sonnet-4-6` to `anthropic/claude-haiku-4-5-20251001`.
- Kept `anthropic/claude-sonnet-4-6` as the only explicit fallback and added both models to the allowlist with aliases:
  - `haiku`
  - `sonnet`
- Cleared the owner Telegram direct/slash sessions so the next real DM starts fresh under the new default model.
- Restarted the gateway successfully through `openclaw gateway restart` after confirming the real service name/path.
- Re-published the Telegram owner menu and added `/model`.
- Sent a completion message into the owner Telegram chat confirming the new model-switch commands.
- Final verified state:
  - `openclaw config validate` passes
  - `openclaw models status --plain` -> `anthropic/claude-haiku-4-5-20251001`
  - `openclaw status --deep` -> gateway reachable, Telegram `ON / OK`
  - owner menu commands:
    - `new`
    - `reset`
    - `model`
    - `status`
    - `restart`
    - `stop`
    - `help`
    - `commands`
  - `sessions.json` now contains only `agent:main:main`
- Residual tradeoff:
  - `openclaw security audit` now warns that `Haiku` is a smaller tier, which is expected and acceptable for the requested cost reduction as long as the owner understands the quality/safety tradeoff.

## 2026-03-28 - OpenClaw Bot Menu and Audio Cleanup

- Continued the external OpenClaw handover autonomously instead of assuming the daemon was still down.
- Re-checked the real live state on `4vps` and found:
  - gateway already healthy on `127.0.0.1:18789`
  - Telegram `ON / OK`
  - the bot still exposed the long default English slash-command menu, including `/restart`
  - status emitted `plugins.entries.audio: plugin not found: audio`
- Confirmed the root cause of the audio warning:
  - `/root/.openclaw/openclaw.json` still had legacy `plugins.entries.audio`
  - current OpenClaw docs now route audio through `tools.media.audio`
  - runtime preflight passed for both Python packages and CLI:
    - `torch`
    - `whisper`
    - `/usr/local/bin/whisper`
- Applied a reversible remote fix:
  - backup created: `/root/.openclaw/openclaw.json.bak_20260328_101740`
  - removed `plugins.entries.audio`
  - added `tools.media.audio.enabled = true`
  - added `tools.media.audio.maxBytes = 20971520`
  - added direct-only audio scope
- Safely restarted OpenClaw and preserved bot availability.
- Replaced the Telegram menu through the Bot API with a compact Russian owner-facing set:
  - `new`
  - `status`
  - `reset`
  - `help`
  - `stop`
- Explicitly did not publish `/resume`, because the current OpenClaw build does not expose it as a supported slash command.
- Final verified state:
  - `openclaw config validate` passes
  - `openclaw status` no longer shows the stale audio-plugin warning
  - gateway reachable on `127.0.0.1:18789`
  - Telegram `ON / OK`
  - security audit remains `0 critical / 1 warn / 1 info`
  - `getMyCommands` returns only the compact menu

## 2026-03-28 - OpenClaw KB Awareness and Owner Menu Upgrade

- Verified that the mounted Obsidian vault was already available to the bot:
  - `/root/.openclaw/workspace/KnowledgeBase` is a symlink to `/root/KnowledgeBase`
  - `rclone-kb.service` is active
  - the mount contains real vault directories and notes
- Found the main cause of the misleading Obsidian answer:
  - remote workspace files still described a generic first-run bot
  - `IDENTITY.md` still referenced the wrong owner
  - the old direct Telegram session still carried stale beliefs
- Corrected the remote workspace source of truth:
  - rewrote `BOOTSTRAP.md`
  - rewrote `IDENTITY.md`
  - rewrote `USER.md`
  - extended `AGENTS.md` with explicit `KnowledgeBase/` access rules
- Cleared the stale direct Telegram session mapping so the next real DM starts from the updated workspace context.
- Restored owner Telegram UX:
  - forced `setChatMenuButton` to `commands`
  - configured compact Russian private commands
  - configured owner-specific Russian commands with `/restart`
  - updated Russian bot description and short description
- Re-enabled `commands.restart = true` intentionally for owner convenience.
- Smoke-tested a fresh session without delivering a message and confirmed the bot now answers correctly about Obsidian access.
- Ran a compact architecture/health pass:
  - `openclaw status --deep` healthy
  - `openclaw security audit --json` still `0 critical / 1 warn / 1 info`
  - `openclaw doctor` initially reported orphan session transcripts and memory-search noise
- Applied cleanup:
  - archived orphan session `.jsonl` files
  - disabled `memorySearch` while no embedding provider exists
- Final state after cleanup:
  - owner menu button = `commands`
  - owner command list:
    - `new`
    - `reset`
    - `status`
    - `restart`
    - `stop`
    - `help`
    - `commands`
  - Telegram `ON / OK`
  - mounted `KnowledgeBase/` is correctly represented in fresh bot responses
  - doctor no longer reports orphan sessions and now reports memory search explicitly disabled

## 2026-03-28 - OpenClaw Security Hardening

- The project was intentionally frozen on `OpenClaw` only; `NemoClaw` is deferred until the VPS plan changes.
- The live `OpenClaw` deployment on `4vps` was hardened to a much narrower single-owner baseline:
  - `sandbox.mode = all`
  - `sandbox.workspaceAccess = none`
  - `tools.profile = messaging`
  - runtime/filesystem/UI/nodes/automation surfaces denied
  - `tools.elevated.enabled = false`
  - Telegram groups disabled
- Host-side file permissions were tightened:
  - `/root/.openclaw` -> `700`
  - config/auth files -> `600`
- Final verified live state:
  - gateway reachable on `127.0.0.1:18789`
  - Telegram `ON / OK`
  - `openclaw security audit --json` -> `0 critical / 1 warn / 1 info`
- Remaining non-blocking notes:
  - only residual audit warning: `gateway.trusted_proxies_missing`
  - sandbox base image is still absent, but current denied tool surface makes that non-blocking
  - memory search has no embedding provider yet
- New documentation artifacts created for continuation and external review:
  - `.agents/handovers/handover_2026-03-28_openclaw-security-hardening.md`
  - `openclaw_project_dossier_2026-03-28.md`
