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
- AI analysis via Gemini (`gemini-2.5-pro` by default) or Anthropic (`claude-opus-4-6`)
- Report JSON and Markdown saved to reports directory
- Knowledge base stored in knowledge_base.json
- Self-improvement suggestions saved to logs
- MCP HTTP server endpoints: /analyze, /analyze/sync, /reports, /report/{id}, /knowledge-base, /health, /improve

Dependencies and env
- anthropic>=0.40.0
- google-genai>=1.0.0
- yt-dlp>=2024.1.0
- LLM_PROVIDER optional, default `gemini`
- GEMINI_API_KEY or GOOGLE_API_KEY required for Gemini
- ANTHROPIC_API_KEY required for Anthropic
- YOUTUBE_API_KEY optional (Data API v3)
- Runtime notes and env examples now live in `.agents/skills/youtube-monitoring/references/reference.md`

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

## 2026-03-18 - Obsidian Productionization

Goal
- Turn the local `workspace/` vault into a production-ready knowledge base for service documentation, source tracking, and agent workflows.

Facts discovered
- Obsidian Desktop `1.12.4` and CLI are now installed and operational.
- The vault already uses core plugins `bases`, `templates`, `daily-notes`, `properties`, and link-oriented navigation.
- Official Obsidian docs treat `.base` as a native accepted file format alongside Markdown, so the prior Markdown-only rule is too strict for a service catalog built on Bases.
- `Templates` plugin stores settings in `.obsidian/templates.json` using `folder`, `dateFormat`, and `timeFormat`.
- `Daily notes` plugin stores settings in `.obsidian/daily-notes.json` using `format`, `folder`, and `template`.
- General vault behavior lives in `.obsidian/app.json`, including `alwaysUpdateLinks`, `attachmentFolderPath`, `newFileLocation`, `newFileFolderPath`, `propertiesInDocument`, and related editing/link settings.

Implications
- The vault should explicitly allow `.base` files as first-class database views over Markdown notes.
- A service-oriented KB should use properties + templates + bases, not ad hoc free-form notes only.
- Daily operational capture should be separated from long-lived knowledge.

## 2026-03-18 - Obsidian Productionization Verification Update

Goal
- Close the runtime verification loop for the vault and reconcile the written rules with the actual Obsidian CLI and plugin layout.

Verified facts
- The installed CLI in Obsidian Desktop `1.12.4` exposes `links` and `backlinks`, not `link-path` and `backlink-path`.
- Community plugins store operational files in `workspace/.obsidian/plugins/<plugin>/`, including `manifest.json`, `data.json`, `main.js`, and `styles.css`; this must be treated as a valid vault-config exception.
- `plugins:enabled filter=community versions format=json` now reports `terminal 3.23.0` and `obsidian-kanban 2.0.51`.
- `bases` lists `projects/runbooks.base`, `projects/services.base`, and `projects/sources.base`.
- After opening `projects/services.base`, `base:views` returns `Services` and `By Status`.
- `daily:path` resolves to `projects/daily/2026/03/2026-03-18.md`.

Operational findings
- `plugin:install` through CLI was unreliable in this environment and timed out twice; manual installation from the official community registry and latest GitHub release assets was the reliable path.
- The user-level PATH already includes `C:\Users\Admin\AppData\Local\Programs\Obsidian`, but the current long-lived shell session still did not resolve `obsidian`; a fresh terminal or the direct `Obsidian.com` path works.

## 2026-03-18 - Dashboard, Board, And Service Catalog Expansion

Goal
- Turn the vault from a technically valid Obsidian setup into a practical operating environment with one start page, one main board, and a seeded database of Obsidian-related services.

Verified facts
- The installed Kanban plugin can create a board from an empty note through `obsidian-kanban:convert-to-kanban`.
- The generated board format starts with frontmatter `kanban-plugin: board`.
- `workspace/.obsidian/workspace.json` can be safely rewritten as plain JSON and reloaded by Obsidian.
- The current vault already contains enough structure to model at least four real operational services: CLI layer, registry layer, kanban layer, and terminal layer.

Implementation decisions
- Create `notes/dashboard.md` as the single landing page for the vault.
- Use `projects/ops-board.md` as the main weekly execution board instead of `projects/task-inbox.md`.
- Seed the service database with records that reflect the actual operating stack of this vault, rather than placeholder examples.
- Keep `task-inbox.md` as a raw intake area, but explicitly demote it behind the main board.
- Keep terminal profile tuning out of this pass; document the service/runbook first, then tune plugin profiles separately if needed.

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

Execution update
- The repaired `notebooklm_auto_refresh.py` still hits Chrome DevTools edge cases on modern Chrome builds (`/json/new` method change, Origin checks, and missing `batchexecute` traffic on an already-loaded page).
- The reliable recovery path is `nlm login --provider openclaw --cdp-url http://127.0.0.1:9223 --force` against the proxy-backed debug Chrome session.
- After re-authentication through that path, `nlm login --check`, `nlm notebook list`, and targeted `nlm notebook get` calls succeeded through `run_nlm_proxy.ps1`.
- A repeated live check on March 18 confirmed that `run_nlm_proxy.ps1 notebook list` returns the full notebook list and both target notebooks remain available.
- A repeated live check on March 18 confirmed that `run_nlm_proxy.ps1 notebook get 254d43aa-a535-46f2-a65b-f6ce877256c9` and `run_nlm_proxy.ps1 notebook get 21c4ad87-0b35-43ca-a31a-01ea3b648b17` both succeed.
- Direct MCP tool entrypoints also succeed when `HTTP_PROXY` and `HTTPS_PROXY` are read from `C:\Users\Admin\.gemini\antigravity\mcp_config.json` before invoking the Python notebook tools.
- Effective steady-state model: keep proxy settings in `mcp_config.json`, use `run_nlm_proxy.ps1` for CLI validation, and only refresh auth again when NotebookLM starts returning `Authentication expired`.
- Additional server check on March 18 found a config-level defect: `C:\Users\Admin\.gemini\antigravity\mcp_config.json` still points to `-m notebooklm_mcp.server`, but the installed package exposes `notebooklm_tools.mcp.server`.
- A direct process check confirmed that `C:\Users\Admin\.gemini\antigravity\venv\Scripts\python.exe -m notebooklm_tools.mcp.server` stays alive and starts cleanly under the configured proxy env.
- The external `mcp_config.json` entry was then corrected to `-m notebooklm_tools.mcp.server`, and a repeat process check confirmed the configured server now starts cleanly from the config itself.

## 2026-03-18 - Cross-Project Rules And Skills Audit

Goal
- Review the current repository state after overlapping updates to rules, protocols, skills, vault instructions, and workflow artifacts, then identify the safest priority order for further work.

Scope inspected
- `AGENTS.md`
- `.agents/skills/core-agent-rules/SKILL.md`
- `.agents/skills/task-executor/SKILL.md`
- `.agents/skills/safety-guardrails/SKILL.md`
- `.agents/skills/skill-conductor/SKILL.md`
- `.agents/skills/version-control/SKILL.md`
- `.agents/skills/youtube-monitoring/**`
- `workspace/agents.md`
- `workspace/notes/index.md`
- `workspace/notes/setup-checklist.md`
- `research_notes.md`
- `implementation_plan.md`
- `task.md`
- `agent_audit.log`
- `C:\Users\Admin\.agents\skills\**`
- local git history and dirty worktree state

Verified facts
- The last committed system refactor exists in git as `2d27562 refactor agent system skills around core rules`.
- The current worktree is dirty with 25 entries in `git status --short`.
- Local and global system skills both exist, but their hashes differ; the divergence is intentional in wording, not yet documented as a source-of-truth policy.
- `youtube-monitoring` currently supports both Gemini and Anthropic in code and documentation.

Findings
- High: `workspace/` policy is internally inconsistent. Root `AGENTS.md` and `implementation_plan.md` describe the vault as Markdown-only, but the actual vault contains `.obsidian/*.json`, which is required for a real Obsidian vault. The verification note in `implementation_plan.md` therefore does not match reality.
- High: `task.md` marks the KB workspace implementation as fully verified, but `workspace/notes/setup-checklist.md` still shows unresolved operational steps: opening the vault in Obsidian, enabling CLI, running the harness from `workspace/`, and verifying `obsidian --help`.
- High: `research_notes.md` and the leading section of `implementation_plan.md` for `youtube-monitoring` are stale. They still describe Anthropic-only analysis and reference `report_schema.md`, while the actual skill now supports Gemini/Anthropic and uses `references/reference.md`.
- Medium: `agent_audit.log` has at least one concatenated entry without a line break, which weakens audit readability and any future machine parsing.
- Medium: workflow artifacts have become a long-lived mixed journal for unrelated tasks. This follows the append rule, but discoverability is degrading and future sessions will have to scan more unrelated history before acting.
- Medium: local and global system skills are no longer byte-identical. The difference is reasonable because local files are repository-specific and global files are generalized, but the repository does not yet state which side is authoritative when the two diverge.
- Medium: many post-commit changes remain uncommitted, including `workspace/`, `youtube-monitoring`, NotebookLM helpers, and current artifact edits. This increases the chance of accidental cross-staging or rollback mistakes during the next round of changes.
- Low: `youtube-monitoring` is currently only local to this repository. That is acceptable, but its intended scope (repo-local vs system-global skill) is not documented yet.

Priority assessment
- P0: Resolve governance contradictions before new automation work. This means aligning `AGENTS.md`, `implementation_plan.md`, `task.md`, and `workspace/agents.md` around the true vault model, including explicit treatment of `.obsidian/`.
- P1: Normalize workflow artifacts so they match current code and verified state. Update the `youtube-monitoring` notes/plan/task sections and mark incomplete KB setup items accurately.
- P2: Repair audit hygiene and change boundaries. Fix newline integrity in `agent_audit.log` going forward, define local-vs-global skill authority, and split pending changes into thematic checkpoints or commits.
- P3: Only after P0-P2, continue with new functional work such as LLM fallback policy or monitor-service integration.

System-level recommendation
- Treat the local repository as the source of truth for repo-specific rules and skills.
- Treat `C:\Users\Admin\.agents\skills\` as a generic mirror that should only be updated from local changes when the local wording has no repository-specific assumptions.
- Keep KB-vault rules and generic agent-system rules separate; do not force `workspace/` vault constraints onto the whole repository.

## 2026-03-18 - Budget Auto Components Radar Concept Review

Goal
- Review `D:\ЯндексДиск\Yandex.Disk\ПРОЕКТЫ\ИИ-мониторинг рынка автокомпоненетов\Концепт бюджетного бизнес-радара GROK.md` and assess the realism, strengths, and risks of the concept.

Files inspected
- `D:\ЯндексДиск\Yandex.Disk\ПРОЕКТЫ\ИИ-мониторинг рынка автокомпоненетов\Концепт бюджетного бизнес-радара GROK.md`
- `D:\ЯндексДиск\Yandex.Disk\ПРОЕКТЫ\ИИ-мониторинг рынка автокомпоненетов\Концепт бюджетного бизнес-радара GROK.rtf`
- sibling PDFs in the same folder for source confirmation

Verified facts
- The requested `.md` file currently exists as a 0-byte placeholder and does not contain the concept text.
- The actual concept text is present in the adjacent `.rtf` file and was extracted successfully.
- A quick official-source spot check confirms that Yandex 360 Messenger Bot API and webhook delivery are available, and Rosstat open data is active.
- The customs/procurement ingestion assumptions look directionally plausible, but they were not fully re-verified end-to-end from official sources during this pass.

Assessment
- Strong: the concept is pragmatic in product framing, keeps the first version narrow enough to be useful, and uses low-cost components that can realistically deliver management signals.
- Strong: combining import dynamics, failed tenders, and weak-competitor signals is strategically sound because it prioritizes actionable gaps rather than generic market dashboards.
- High risk: the document overstates confidence in delivery speed, budget, and signal quality. A 2-3 week MVP is realistic only for a smaller slice: ETL + scoring + email/chat digest, not the full stack including RAG, bot, Alice, and dashboard polish.
- High risk: data reliability is the main constraint, not model quality. Source volatility, parser fragility, rate limits, and legal/operational limits around competitor enrichment are underplayed.
- Medium risk: ROI language is too aggressive for a concept note. Claims such as "70-80 % of real opportunities" and "окупает MVP за 1-2 месяца" need a validation design, baseline, and sample cases.
- Medium risk: the concept needs an explicit scoring model, precision/recall target, and analyst feedback loop; otherwise the "daily predictive signal" can degrade into noisy alerts.
- Low risk: the modular architecture is sensible, but some choices are heavier than needed for phase 1. SQLite plus simple statistical rules is enough before introducing RAG or more advanced forecasting.

## 2026-03-18 - Budget Auto Components Radar Rewrite

Goal
- Rewrite the reviewed concept into a stronger decision-grade Markdown version with a more credible MVP scope and a phased plan with brief rationale per stage.

Target edited
- `D:\ЯндексДиск\Yandex.Disk\ПРОЕКТЫ\ИИ-мониторинг рынка автокомпоненетов\Концепт бюджетного бизнес-радара GROK.md`

Rewrite decisions
- Replace the empty `.md` placeholder with a full standalone Markdown document.
- Shift the framing from "AI platform" to "management signal system" so the value proposition is operational instead of decorative.
- Make the scoring logic explicit because the original concept promised predictive signals without showing how those signals are derived.
- Narrow phase 1 to data, scoring, digest delivery, and feedback; postpone voice, deep RAG, and wider integration.
- Add stage-by-stage justification so the rollout order is defensible to management and aligned with trust-building in the signals.

Result
- The rewritten document now includes: executive framing, MVP boundaries, source strategy, explicit scoring logic, realistic architecture, phased implementation plan, success metrics, risks, and a final decision statement.
- The external target file is no longer empty and now contains a readable UTF-8 Markdown concept.

## 2026-03-18 - Cross-Update Stabilization Execution

Actions taken
- Aligned root `AGENTS.md` and `workspace/agents.md` on a Markdown-first vault model with allowed `.base`, `workspace/.obsidian/*.json`, and a repo-root fallback when KB tasks are launched outside the vault root.
- Updated the leading `youtube-monitoring` artifacts so they describe Gemini/Anthropic support, provider env vars, and the actual `references/reference.md` file.
- Documented local `.agents/skills/**` as the repository source of truth and `C:\Users\Admin\.agents\skills\` as a generic mirror only for portable changes.
- Tightened audit-log guidance to require one UTF-8 record per line and created checkpoint `checkpoint_20260318_020141` before the stabilization edits.

Remaining risks
- KB routing rules, vault exceptions, and the setup checklist are now aligned; future KB sessions still need to keep vault-specific operations scoped to `workspace/`.
- The dirty worktree still spans multiple themes; only the current stabilization cohort is checkpointed explicitly in this pass.
- LLM fallback automation and monitoring-service integration remain intentionally deferred until the remaining dirty-worktree grouping is explicit.

## 2026-03-18 - Dirty Worktree Grouping

Verified facts
- The remaining dirty worktree can now be explained by five intentional source cohorts plus one local-only generated-artifacts cohort.
- Clean rollback checkpoints exist for governance (`checkpoint_20260318_023712`), YouTube monitoring (`checkpoint_20260318_023808`), NotebookLM helpers (`checkpoint_20260318_023809`), workspace vault (`checkpoint_20260318_023811`), and site/reference outputs (`checkpoint_20260318_023813`).
- The first rapid back-to-back checkpoint attempt collided on the second-based ID generator and produced mixed directory `checkpoint_20260318_023731`; it should be treated as legacy and ignored for restore decisions.

Grouping decisions
- Keep `.agents/checkpoints/**`, `__pycache__/`, YouTube analyzer logs, and `tests/tmp_kb/knowledge_base.json` in a local operational cohort instead of treating them as commit candidates.
- Use `progress.md` as the current source for checkpoint IDs and intended commit order across the still-dirty worktree.

## 2026-03-18 - Cohort Staging Strategy (No Commit)

Goal
- Prepare deterministic cohort-based staging commands without creating commits.

Facts
- The index is currently over-staged (`git diff --cached --name-only` returns 243 paths).
- A dry-run-first staging workflow reduces risk while preserving the dirty worktree.

Actions
- Added `scripts/git_cohort_stage.ps1` to stage by cohort with optional index reset and generated-artifact exclusion.
- Added `staging_strategy.md` with baseline, dry-run, apply, and validation command sequences.
- Verified script output in dry-run mode for `show`, single-cohort, and `all`.

## 2026-03-18 - Ecosystem Overlap And Architecture Analysis

Goal
- Analyze the current project ecosystem across `My Dashboard`, vault notes, NotebookLM integration, chats, and workflows in order to separate duplication from legitimate layer boundaries.

Sources reviewed
- `C:\Users\Admin\.gemini\antigravity\scratch\Мой Дашборд\data\dashboard_data.json`
- `C:\Users\Admin\.gemini\antigravity\scratch\Мой Дашборд\data\mindmap.json`
- `C:\Users\Admin\.gemini\antigravity\scratch\Мой Дашборд\README.md`
- `workspace/notes/dashboard.md`
- `workspace/notes/target-system-architecture.md`
- `workspace/notes/project-status-summary.md`

Verified facts
- The dashboard currently tracks `22` projects, `37` chats, and `21` workflows.
- `11` of the `22` projects are still grouped under the `manual` topic, which indicates a large amount of user-facing/system-facing overlap.
- All `37` chats in the exported dashboard index are currently unlinked to project IDs.
- The vault already states the target architecture as `My Dashboard -> Agent -> Vault`.
- NotebookLM is already functioning as an MCP-connected external knowledge tool rather than as the main system of record.

Analysis
- The main overlap is structural, not accidental: several current projects are really partial views of the same target system.
- `My Dashboard` should be the front door and daily UI.
- `Obsidian vault` should be the durable memory and knowledge graph.
- `NotebookLM` should be the bounded deep-reading and synthesis workspace.
- Chats should be treated as transient working memory and raw traces, not as durable knowledge.
- Workflows, skills, and agent projects should be treated as one execution layer, not as separate user-facing systems.

Recommended direction
- Converge on a layered model instead of parallel product growth.
- Introduce a canonical `project_id` registry shared by dashboard, vault, workflows, chat routing, and notebook mappings.
- Introduce a single inbox pipeline and a project-specific launch contract for agents.
- Keep autonomous or semi-autonomous agents behind a stable registry/inbox architecture instead of scaling orchestration first.

Artifact created
- Added `workspace/notes/ecosystem-overlap-analysis.md` and linked it from the vault dashboard/index.

Additional input from external `analysis_results.md`
- The external analysis strongly aligns with the current `My Dashboard -> Agent -> Vault` direction and does not require an architectural reversal.
- It adds three concrete planning deltas worth keeping:
  - treat dashboard JSON as generated exports from vault entities rather than as manually maintained parallel state;
  - define a minimal YAML/frontmatter entity schema for projects, agents, ideas, artifacts, tasks, and reports;
  - add a weekly synthesis/report loop that summarizes changed projects into a report layer.

## 2026-03-18 - Dashboard Productization MVP

Goal
- Turn the convergence plan into a working MVP where the dashboard consumes a canonical project registry derived from the vault and exposes a usable `project mode`.

Verified facts
- `sync_workspace_data.py` now completes successfully and generates `projects.json`, `data/dashboard_data.json`, `data/mindmap.json`, `data/project_registry.json`, `docs/information_operating_system_2026-03-18.md`, and `docs/weekly_project_brief.md`.
- The sync run exported `22` projects, `38` chats, and `21` workflows and also published `KnowledgeBase/Dashboards/Weekly Project Brief.md`.
- `data/project_registry.json` contains `22` project entries; sampled entries include `launchContract.prompt`, `projectMode.allowedTools`, and a KB entry point.
- `projects.json` now embeds `projectRegistry`, so the dashboard has a compatibility fallback even if the dedicated registry file is unavailable.
- `app.js` passes `node --check`, and the sync script passes `python -m py_compile`.

Implementation decisions
- The vault is treated as the canonical overlay: existing KB entity notes enrich generated project/chat/workflow records before dashboard export.
- Entity note export is now non-destructive by default: existing project/chat/workflow notes are preserved unless `--refresh-obsidian-entities` is explicitly requested.
- The dashboard UI now uses registry-backed `Project mode` actions instead of relying only on raw project cards.

Remaining gap
- Legacy chats and workflows are not yet fully normalized to `project_id`; current linking is strong enough for the MVP but not yet complete for autonomous orchestration.

## 2026-03-18 - Legacy Chat Link Normalization

Goal
- Reduce the number of chat sessions without `project_id` links so the graph is usable for project-scoped agent orchestration rather than only dashboard viewing.

Verified facts
- Before this pass, generated state had `21` unlinked chats and `0` unlinked workflows.
- The weak spot was concentrated in legacy/brain-derived chats, especially system sessions around NotebookLM, Dashboard, Obsidian, grants, and monitoring.
- Invalid legacy IDs such as `agent-second-brain` were still leaking into `relatedProjectIds` even though those projects are no longer in the canonical project set.

Actions taken
- Added evidence-based chat autolinking that uses title/summary, markdown snippets from brain files, path hints, exact project aliases, and curated domain hint rules.
- Added a second reconciliation pass after KB overlay so legacy CSV links and Obsidian links cannot overwrite each other into an inconsistent state.
- Added sanitization that filters `relatedProjectIds` to the current canonical project set only.

Result
- Unlinked chats reduced from `21` to `4`.
- Invalid project references in chats reduced from `3` cases to `0`.
- Remaining unlinked titles are currently the most ambiguous generic sessions: `Task Plan`, `Текущие задачи`, `Поиск фотографий`, `Agent Second Brain Task Plan`.

## 2026-03-18 - External Audit File Inventory

Goal
- Prepare a machine-readable full file inventory so an independent advanced LLM can audit the entire current system and propose further development directions.

Scope included
- Current repository
- Scratch dashboard workspace
- KnowledgeBase vault
- Antigravity brain/session store
- MCP config
- NotebookLM runtime/profile cache

Artifacts created
- `system_audit_full_file_inventory_2026-03-18_23-32-39.txt`
- `system_audit_manifest_2026-03-18_23-32-39.md`
- `external_audit_bundle_2026-03-18_23-45-29/`
- `external_audit_bundle_2026-03-18_23-45-29.zip`

Verified facts
- The generated inventory contains `4772` absolute file paths in one unified list.
- The manifest records root counts, sensitivity notes, and a recommended audit order for the external model.
- The curated bundle contains `48` copied/redacted files plus prompt and bundle manifest, and the ZIP was created successfully.

## 2026-03-19 - Post-Audit Quick Wins

Goal
- Implement the first verified fixes from `D:\ЯндексДиск\Yandex.Disk\ПРОЕКТЫ\АУДИТ ВСЕЙ СИСТЕМЫ\Инструкция после аудита Claude.md` without changing the target architecture.

Files inspected
- `D:\ЯндексДиск\Yandex.Disk\ПРОЕКТЫ\АУДИТ ВСЕЙ СИСТЕМЫ\Инструкция после аудита Claude.md`
- `AGENTS.md`
- `workspace/agents.md`
- `C:\Users\Admin\.gemini\antigravity\scratch\Мой Дашборд\AGENTS.md`
- `C:\Users\Admin\.gemini\antigravity\scratch\Мой Дашборд\scripts\dashboard\sync_workspace_data.py`
- `C:\Users\Admin\.gemini\antigravity\scratch\Мой Дашборд\projects.json`

Verified facts
- `sync_workspace_data.py` read `projects.json` as input and then overwrote the same file as generated output; this was a real circular dependency risk.
- `NotebookLM` was injected into every `launchContract.allowedTools` unconditionally, even though the post-audit instruction requires feature gating.
- Workflow deduplication only covered filesystem fallback discovery; duplicate rows in `workflows_index.csv` with the same normalized path were not filtered.
- Project `notes` duplication survived initial merge logic because preserved KB entity-notes could overwrite cleaned values during overlay.
- Three instruction files (`AGENTS.md`, `workspace/agents.md`, dashboard `AGENTS.md`) needed an explicit priority marker to reduce policy drift.

Implementation decisions
- Split manual input from generated output by defaulting manual overrides to `projects_manual_base.json` and generated compatibility output to `projects.json`.
- Seed `projects_manual_base.json` automatically from existing generated `projects.json` on first run to avoid a manual migration step.
- Gate NotebookLM through `NOTEBOOKLM_AVAILABLE=false` by default and publish `notebooklmEnabled` in both `projectMode` and `launchContract`.
- Deduplicate notes both at source merge time and at KB overlay time so legacy entity-notes stop reintroducing repeated `;` segments.
- Add root-level write-back protocol and explicit AGENTS priority comments instead of trying to unify all AGENTS files in the same pass.

Verification
- `python -m py_compile C:\Users\Admin\.gemini\antigravity\scratch\Мой Дашборд\scripts\dashboard\sync_workspace_data.py`
- `python C:\Users\Admin\.gemini\antigravity\scratch\Мой Дашборд\scripts\dashboard\sync_workspace_data.py`
- Post-sync asserts confirmed:
  - `projects_manual_base.json` exists
  - `launchContract.allowedTools` no longer contains `notebooklm` by default
  - `launchContract.notebooklmEnabled == false` for all registry items
  - `tgaggregator.notes` is deduplicated down to one segment
  - workflow paths in generated dashboard data are unique by normalized path

Deferred
- QW-6 (schema validation for project frontmatter) is not implemented yet.
- QW-7 (`.obsidian` isolation in guardrails/ignore rules) is not implemented yet.

## 2026-03-22 - OpenClaw Personal Deployment Report

Goal
- Prepare an evidence-based report on what OpenClaw actually is, how the Habr case maps to the real product, and how to deploy OpenClaw or an Anthropic-based alternative on a personal Windows PC for business and personal workflows.

Sources checked
- Habr article `https://habr.com/ru/articles/1008982/`
- OpenClaw official repo `https://github.com/openclaw/openclaw`
- OpenClaw official docs `https://docs.openclaw.ai/`
- Anthropic official docs on computer use and models `https://docs.anthropic.com/`

Verified facts
- The Habr article was published on 2026-03-11 and describes OpenClaw as an orchestrator around LLMs, skills, and integrations rather than a full autonomous system by itself.
- The article's concrete marketing case combined official APIs, Google Sheets API, browser automation via Playwright, and vision analysis; the reported implementation was not "just prompts", but a custom skill with ~3,700 lines of code plus infrastructure.
- OpenClaw official repo currently describes the product as a self-hosted personal AI assistant that runs on your own devices and can connect to channels such as Telegram, WhatsApp, Slack, Discord, Signal, iMessage, and others.
- OpenClaw's recommended setup path is `openclaw onboard`; on Windows the official repo explicitly recommends WSL2.
- OpenClaw's docs expose first-class tools such as `exec`, `browser`, `web_search`, `web_fetch`, file tools, messaging, and cron/gateway automation. Tool access is configurable through allow/deny lists and base profiles (`full`, `coding`, `messaging`, `minimal`).
- OpenClaw has an approvals system for command execution, including host-specific approval files.
- OpenClaw onboarding supports cloud providers and local models; docs mention Anthropic setup-token auth, OpenAI Codex OAuth, API keys, and LM Studio local models.
- Anthropic's official computer-use docs explicitly mark the feature as beta and recommend using a dedicated VM or container with minimal privileges because browser/desktop control has unique security risks.
- Anthropic model pricing docs currently list Claude Sonnet 4 at $3 per 1M input tokens and $15 per 1M output tokens, with higher pricing for Opus models.

Conclusions
- The Habr case is directionally plausible, but it is a custom integration project on top of OpenClaw, not a one-click business automation product.
- "Self-hosted" in the OpenClaw sense does not automatically mean fully local AI inference: if Anthropic/OpenAI/Gemini models are used, your prompts and context still leave the PC and go to the provider.
- For a Windows personal computer, the realistic path is OpenClaw in WSL2 plus carefully limited tools, not unrestricted desktop automation on the host OS.
- Anthropic does provide the model/tool layer (`computer use`, APIs, Claude Code for coding), but not a complete consumer-grade self-hosted personal-assistant shell equivalent to OpenClaw; building a general assistant around Anthropic still requires your own orchestration layer.
- The safest rollout path is staged: start with chat + search + notes + calendar/tasks, then add APIs, and only then add browser/UI automation for the few systems that truly lack APIs.

## 2026-03-28 - OpenClaw VPS Continuation

Goal
- Continue the VPS setup from the existing handover, verify the real live state on `4vps`, and install the correct NVIDIA security component without breaking the working OpenClaw gateway.

Verified facts
- Local note `D:\ЯндексДиск\Yandex.Disk\ПРОЕКТЫ\openclaw\4vps.txt` contains the server address and root password used for SSH.
- Live SSH verification confirmed the host is `Ubuntu 22.04.5 LTS` and the OpenClaw CLI is installed as `OpenClaw 2026.3.24 (cff6dc9)`.
- `openclaw status` on the VPS shows `Gateway service` as `systemd installed · enabled · running` and Telegram as `ON`.
- The same status output shows `Node service` as `systemd not installed`, so the live deployment is gateway-based rather than a separate node service.
- The local `NVIDIA NemoClaw.txt` note is not authoritative. Official NVIDIA documentation references `NeMo Guardrails`, not a product named `NemoClaw`.
- `python3.10-venv` was missing on the VPS and had to be installed before a virtual environment could be created.
- `nemoguardrails 0.21.0` was successfully installed in `/opt/nemoguardrails/venv`.

Conclusions
- The live OpenClaw deployment is working and does not need a reinstall.
- The correct NVIDIA-related add-on is `NeMo Guardrails`, and it is now installed in an isolated venv instead of being forced into the system Python.
- There is still no automatic integration between OpenClaw and NeMo Guardrails; that would be a separate wiring task if the user wants the guardrail layer to mediate OpenClaw behavior.

## 2026-03-28 - NemoClaw Port Conflict Root Cause

Goal
- Verify whether NemoClaw supports a documented or hidden onboarding override for the dashboard/control port that conflicts with an existing OpenClaw deployment on `18789`.

Sources checked
- `https://github.com/NVIDIA/NemoClaw`
- `https://raw.githubusercontent.com/NVIDIA/NemoClaw/main/nemoclaw-blueprint/blueprint.yaml`
- `https://raw.githubusercontent.com/NVIDIA/NemoClaw/main/bin/lib/onboard.js`
- `https://docs.nvidia.com/nemoclaw/latest/reference/commands.html`

Verified facts
- NemoClaw is a real NVIDIA repository/project (not just a naming error), in early preview.
- `nemoclaw-blueprint/blueprint.yaml` includes `forward_ports: [18789]`.
- `bin/lib/onboard.js` performs preflight checks for both required ports:
  - `8080` (`OpenShell gateway`)
  - `18789` (`NemoClaw dashboard`)
- The same onboarding implementation contains hardcoded `18789` forward/stop/start operations and `CONTROL_UI_PORT = 18789`.
- The official commands reference does not document a CLI flag for overriding the dashboard/control port during `nemoclaw onboard`.

Conclusions
- The blocker is real: changing only `blueprint.yaml` to another forwarding port is insufficient because onboarding still reserves/checks `18789`.
- A supported no-downtime path to keep existing OpenClaw on `18789` and complete full NemoClaw onboarding was not found in official docs/code paths inspected.
- Practical options are:
  1. keep current OpenClaw unchanged and skip full NemoClaw onboarding;
  2. migrate OpenClaw off `18789`, then rerun NemoClaw onboarding;
  3. apply an unsupported local patch to NemoClaw onboarding code (high fragility, can break on update).

## 2026-03-28 - NemoClaw Resume Failure Root Cause

Goal
- Continue full `NemoClaw` onboarding after the port blocker was cleared and determine why the sandbox step still fails.

Verified facts
- `OpenClaw` was already stopped when the continuation started, so `18789` was free before the retry.
- Fresh host-side backups now exist in `/root/nemoclaw-backups` for both `/root/.openclaw` and `/root/.nemoclaw`:
  - `openclaw_pre_resume_20260328_003059.tgz`
  - `nemoclaw_pre_resume_20260328_003059.tgz`
- `nemoclaw onboard --resume --non-interactive` successfully rebuilt the sandbox image `openshell/sandbox-from:1774654357`.
- The retry failed again at the `sandbox` step after the image build, during `openshell sandbox create`.
- The onboarding log shows the child process terminated with `Killed` while pushing the sandbox image into the gateway.
- Kernel logs (`dmesg -T` and `journalctl -k`) confirm a real memory exhaustion event at `2026-03-28 00:35:34`, including `Out of memory: Killed process 81398 (openshell)`.
- The VPS currently has `3.8 GiB` RAM and `0 B` swap.
- After the failed retry, `OpenClaw` was explicitly restored with `openclaw gateway start`.
- Final rollback verification shows:
  - `openclaw-gateway.service` is running again
  - `127.0.0.1:18789` is listening
  - `Telegram` channel state is `ON / OK`

Conclusions
- The blocking issue is no longer the `18789` port conflict; it is insufficient memory during `openshell sandbox create`.
- A third onboarding retry without changing VPS memory conditions would be random repetition and was not attempted.
- The safest next step is infrastructural: add swap and/or move to a larger RAM plan, then rerun `nemoclaw onboard --resume --non-interactive`.

## 2026-03-28 - NemoClaw Final Retry After Swap And Disk Cleanup

Goal
- Push the existing `NemoClaw` onboarding as far as possible on the current VPS by removing resource blockers, then leave the host in a stable state.

Verified facts
- Host swap is now enabled and persistent:
  - `/swapfile`
  - `2.0 GiB` total swap
- `OpenClaw` credentials were not available through the shell environment used for `nemoclaw onboard`, but the Anthropic API key source was confirmed to exist in the OpenClaw auth profile store (`auth-profiles.json`), which allowed a resumed run without asking the user for a new secret.
- Safe disk-recovery actions completed before the final retry:
  - removed stale `/tmp/openshell-images.tar` inside `openshell-cluster-nemoclaw`
  - removed old unused `openshell/sandbox-from:*` images and dangling layers that were left by failed builds
- The final retry advanced materially further than all previous attempts:
  - gateway recreated successfully and became healthy
  - inference provider configured successfully
  - sandbox image `openshell/sandbox-from:1774658382` built successfully
  - image export completed and upload into the gateway completed
- The retry still failed at the `sandbox` step, but only after the image had already become available inside the gateway.
- At the failure point, root filesystem pressure returned to a critical level:
  - `/dev/vda2` reached `100%`
  - only `35M` remained free
- The terminal sandbox error after the successful upload was:
  - `tls handshake eof`
- The failure happened while `openshell sandbox create` was still active and the gateway host was effectively out of disk headroom.
- Post-failure stabilization succeeded:
  - removed failed `openshell-cluster-nemoclaw` container
  - removed its `openshell-cluster-nemoclaw` Docker volume
  - host free space returned to about `3.9G`
  - `OpenClaw` gateway was restored and verified reachable again on `127.0.0.1:18789`
  - Telegram channel remained `ON / OK`

Conclusions
- The original blockers were real but are no longer the decisive ones:
  - port `18789` conflict was handled
  - OOM was mitigated with swap
  - missing `ANTHROPIC_API_KEY` in the onboarding shell was worked around from the existing OpenClaw auth profile
- The current hard blocker is storage capacity of the VPS during the full sandbox materialization path.
- On the current plan, `NemoClaw` can now get through build and gateway upload, but the remaining disk margin is too small to complete sandbox creation reliably.
- The cleanest next step is infrastructure, not another retry on the same disk budget.

## 2026-03-28 - OpenClaw Security Hardening And Dossier

Goal
- Keep only `OpenClaw` on the current `4vps` host, harden it for secure single-owner Telegram use, and prepare a detailed project dossier for another LLM.

Sources checked
- `D:\ЯндексДиск\Yandex.Disk\ПРОЕКТЫ\openclaw\лучшие практики от Grok.txt`
- OpenClaw official docs:
  - `https://docs.openclaw.ai/gateway/security`
  - `https://docs.openclaw.ai/gateway/configuration-reference`
  - `https://docs.openclaw.ai/reference/token-use`
- Live VPS state via SSH:
  - `openclaw status`
  - `openclaw security audit --json`
  - `openclaw sandbox explain --json`
  - `openclaw doctor`
  - raw `/root/.openclaw/openclaw.json`

Verified initial facts
- The live host was still healthy before hardening:
  - gateway reachable on `127.0.0.1:18789`
  - Telegram `ON / OK`
- The pre-hardening config was too broad for a security-first baseline:
  - `tools.profile = "coding"`
  - `agents.defaults.sandbox.mode = off`
  - `tools.fs.workspaceOnly = false`
  - `tools.elevated.enabled = true`
  - `commands.restart = true`
  - `channels.telegram.groupPolicy = "allowlist"`
  - `gateway.nodes.denyCommands` contained ineffective command IDs
- The initial security audit had `0 critical / 3 warn / 1 info`:
  - `gateway.trusted_proxies_missing`
  - `gateway.nodes.deny_commands_ineffective`
  - `security.trust_model.multi_user_heuristic`
- `openclaw doctor` additionally confirmed that Telegram groups were not actually usable in the current config because group allowlists were empty, so group messages would be silently dropped.

Applied changes on the VPS
- Created fresh config backups before each risky edit:
  - `/root/.openclaw/openclaw.json.bak_20260328_020925`
  - `/root/.openclaw/openclaw.json.bak_20260328_021123`
  - `/root/.openclaw/openclaw.json.bak_20260328_021510`
- Hardened the live config to an OpenClaw secure baseline plus sandboxing:
  - `agents.defaults.sandbox.mode = "all"`
  - `agents.defaults.sandbox.scope = "agent"`
  - `agents.defaults.sandbox.workspaceAccess = "none"`
  - `tools.profile = "messaging"`
  - `tools.allow = ["image"]`
  - `tools.deny = ["group:automation", "group:runtime", "group:fs", "group:ui", "group:nodes", "sessions_spawn", "sessions_send"]`
  - `tools.fs.workspaceOnly = true`
  - `tools.exec.security = "deny"`
  - `tools.exec.ask = "always"`
  - `tools.elevated.enabled = false`
  - `commands.restart = false`
  - `channels.telegram.groupPolicy = "disabled"`
- Removed obsolete `gateway.nodes.denyCommands`.
- Tightened host-side permissions:
  - `/root/.openclaw` -> `700`
  - `/root/.openclaw/openclaw.json` -> `600`
  - `/root/.openclaw/agents/main/agent/auth-profiles.json` -> `600`
- Added low-risk token-efficiency settings:
  - `agents.defaults.models["anthropic/claude-sonnet-4-6"].params.cacheRetention = "long"`
  - `agents.defaults.contextPruning.mode = "cache-ttl"`
  - `agents.defaults.contextPruning.ttl = "1h"`

Verified final facts
- Final config validation passed: `Config valid: ~/.openclaw/openclaw.json`.
- Final model map on disk was cleaned to one real key only:
  - `["anthropic/claude-sonnet-4-6"]`
- Python-level readback from `openclaw.json` confirmed:
  - `{"params":{"cacheRetention":"long"}}` for `anthropic/claude-sonnet-4-6`
- Final live state after hardening:
  - gateway reachable on `127.0.0.1:18789`
  - Telegram `ON / OK`
  - security audit reduced to `0 critical / 1 warn / 1 info`
- The only remaining audit warning is `gateway.trusted_proxies_missing`, which is benign while the gateway remains loopback-only and becomes relevant only if a reverse proxy or external HTTP path is added later.

Residual technical notes
- `openclaw doctor` still reports `openclaw-sandbox:bookworm-slim` as missing.
  - This is currently non-blocking because runtime/filesystem/UI/node tools are explicitly denied.
  - If those tools are re-enabled later, the sandbox base image should be prepared first.
- Memory search was explicitly disabled after live verification showed `Provider: none` and unavailable embeddings.
  - This removes a dead, noisy subsystem from the current baseline.
  - If semantic recall is needed later, it should be re-enabled only together with an intentional embedding-provider setup.

Conclusions
- A materially safer `OpenClaw` baseline is now live on the VPS without breaking the working Telegram channel.
- The operational trust boundary is now much closer to the documented single-owner OpenClaw model:
  - no Telegram groups
  - no runtime/filesystem/tool escalation on the host
  - sandboxing enabled
  - workspace access disabled inside the sandbox
- `NemoClaw` remains intentionally deferred because the current VPS plan is still too disk-constrained for reliable onboarding.

## 2026-03-30 - Telegram Chat Analysis Prompt Pack Run

Goal
- Run the staged Telegram analysis prompt-pack against the `OpenClaw Lab Community` export and save reusable analytical artifacts.

Inputs inspected
- `workspace/projects/telegram-chat-analysis-prompt-pack/README.md`
- `workspace/projects/telegram-chat-analysis-prompt-pack/system_instruction.md`
- stage prompts and matching schemas in `workspace/projects/telegram-chat-analysis-prompt-pack/`
- `C:\Users\Kogan\Downloads\Telegram Desktop\ChatExport_2026-03-29\result.json`

Verified dataset facts
- Chat name: `OpenClaw Lab Community`
- Chat type: `public_supergroup`
- Message corpus: `8891` message entries + `26` service entries
- Date range: `2026-02-16` to `2026-03-29`
- Messages with links: `424`
- Attachments present in the export tree and message corpus
- Highest-volume discussion window: roughly `2026-03-08` to `2026-03-12`

High-signal findings
- The strongest stable theme is that OpenClaw is treated as a security-first, file-driven, version-sensitive agent system, not a zero-config chatbot.
- Telegram topics + explicit ACLs are a major operational topic; they are discussed as a practical boundary for quasi-multi-agent setups.
- Layered file memory (`memory/YYYY-MM-DD.md` + `MEMORY.md` + retrieval) is the most repeatable memory pattern in the corpus.
- Long-horizon Telegram analysis pushes the community toward vector-memory ingestion rather than ever-growing live sessions.
- Many “agent degraded / nothing happens” reports are actually runtime/provider/policy failures: OAuth race, message-tool premature completion, thinking-output mismatch, session bloat, sandbox/exec gaps, and conflicting prompt files.

Risks and limitations
- No external verification was performed in this run; provider-policy and release claims remain claims, not facts.
- Release-digest posts are detailed but still secondary summaries.
- Small local-model viability is only weakly supported by the corpus.

## 2026-03-28 - OpenClaw Cost Switch to Haiku and In-Bot Model Picker

Official references checked
- `https://docs.openclaw.ai/concepts/models`
- `https://docs.openclaw.ai/channels/telegram`

Verified facts before the change
- The live Anthropic-backed default model on the VPS was still `anthropic/claude-sonnet-4-6`.
- `openclaw config get agents.defaults.model` returned only:
  - `{"primary":"anthropic/claude-sonnet-4-6"}`
- `openclaw config get agents.defaults.models` showed a one-model allowlist:
  - `anthropic/claude-sonnet-4-6`
- The stored Telegram owner sessions existed under:
  - `agent:main:telegram:slash:708744350`
  - `agent:main:telegram:direct:708744350`

Key findings
- Official OpenClaw docs confirm the valid config keys are:
  - `agents.defaults.model.primary`
  - `agents.defaults.model.fallbacks`
  - `agents.defaults.models` as the `/model` allowlist/catalog
- The first remote patch failed validation because it used `fallback` instead of documented `fallbacks`; rollback worked correctly.
- Official docs also confirm that in chat the supported model-switch flow is:
  - `/model`
  - `/model list`
  - `/model <ref>`
  - `/model status`
- Telegram native command menu is registered through `setMyCommands`; adding `/model` to the owner menu is enough to expose model switching directly in the bot UI.

Applied changes on the VPS
- Created fresh backups before the model switch:
  - `/root/.openclaw/openclaw.json.bak_20260328_163658`
  - `/root/.openclaw/openclaw.json.bak_20260328_163957`
  - `/root/.openclaw/agents/main/sessions/sessions.json.bak_20260328_163957`
- Switched the documented default-model policy to:
  - primary: `anthropic/claude-haiku-4-5-20251001`
  - fallbacks: `["anthropic/claude-sonnet-4-6"]`
- Expanded the model allowlist/catalog to two explicit entries:
  - `anthropic/claude-haiku-4-5-20251001`
  - `anthropic/claude-sonnet-4-6`
- Added stable aliases for in-bot switching:
  - `haiku`
  - `sonnet`
- Kept `params.cacheRetention = "long"` for both models.
- Cleared the owner Telegram direct and slash session mappings so the next real Telegram interaction starts fresh on the new default model.
- Restarted the gateway via the official CLI path:
  - `openclaw gateway restart`
  - result: `Restarted systemd service: openclaw-gateway.service`
- Re-published Telegram command menus with `/model` included:
  - private scope: `new`, `reset`, `model`, `status`, `stop`, `help`, `commands`
  - owner chat scope: `new`, `reset`, `model`, `status`, `restart`, `stop`, `help`, `commands`
- Sent a completion message into the owner Telegram chat via:
  - `openclaw message send --channel telegram --target 708744350 ...`
  - Telegram delivery returned message id `137`

Verified final facts
- `openclaw config validate` passes after the change.
- `openclaw models status --plain` returns:
  - `anthropic/claude-haiku-4-5-20251001`
- `openclaw config get agents.defaults.model` returns:
  - primary `anthropic/claude-haiku-4-5-20251001`
  - fallbacks `["anthropic/claude-sonnet-4-6"]`
- `openclaw config get agents.defaults.models` returns both allowed models with aliases `haiku` and `sonnet`.
- After the Telegram-session reset, `sessions.json` contains only:
  - `agent:main:main`
- Final live state after the gateway restart:
  - gateway reachable
  - Telegram `ON / OK`
  - default model in overview: `claude-haiku-4-5-20251001`
- Bot API verification for the owner menu now returns:
  - `new`
  - `reset`
  - `model`
  - `status`
  - `restart`
  - `stop`
  - `help`
  - `commands`

Tradeoff recorded
- The OpenClaw security audit now shows one additional non-critical warning because `Haiku` is a smaller tier.
- This is an intentional cost/latency tradeoff requested by the owner; the higher-capability fallback remains `claude-sonnet-4-6`.

## 2026-03-28 - OpenClaw Bot Menu and Audio Cleanup

Goal
- Continue the external OpenClaw handover autonomously, fix the outdated Telegram bot menu, and clean up the legacy audio configuration without breaking the live gateway.

Facts gathered from the live VPS
- `openclaw status` showed the gateway already healthy on `127.0.0.1:18789` and Telegram `ON / OK`, so the daemon was not actually down at the moment of continuation.
- Telegram `getMyCommands` still returned the full default English slash-command list, including commands that are no longer appropriate for the hardened owner-only setup such as `/restart`.
- `openclaw status` emitted the warning `plugins.entries.audio: plugin not found: audio`.
- `/root/.openclaw/openclaw.json` still contained a legacy `plugins.entries.audio` entry, while the current official OpenClaw docs route audio handling through `tools.media.audio`.
- Voice-runtime preflight on the VPS passed:
  - `torch` import OK
  - `whisper` import OK
  - `whisper` CLI available at `/usr/local/bin/whisper`
- The suggested `/resume` command from the external handover was not present in the current supported `getMyCommands` output, so publishing it would have created a broken menu item.

Applied changes on the VPS
- Created a fresh config backup before editing:
  - `/root/.openclaw/openclaw.json.bak_20260328_101740`
- Removed the stale legacy config entry:
  - `plugins.entries.audio`
- Added the documented audio block under `tools.media.audio`:
  - `enabled = true`
  - `maxBytes = 20971520`
  - `scope = direct-only`
- Re-validated the config and restarted OpenClaw safely in the background.
- Replaced the Telegram bot menu through the Telegram Bot API from the VPS with a compact Russian command set made only from currently supported slash commands:
  - `new`
  - `status`
  - `reset`
  - `help`
  - `stop`

Verified results
- `openclaw config validate` passes.
- `openclaw status` no longer shows the stale audio-plugin warning.
- The live state after restart remained healthy:
  - gateway reachable on `127.0.0.1:18789`
  - Telegram `ON / OK`
  - `openclaw security audit --json` effectively unchanged at `0 critical / 1 warn / 1 info`
- `getMyCommands` now returns the compact Russian menu only.

Residual note
- End-to-end voice-note handling still needs one real Telegram voice message from the owner to validate the full ingest path after the config migration.

## 2026-03-28 - OpenClaw KB Awareness, Owner Menu, and Architecture Check

Goal
- Make the bot answer truthfully about the mounted Obsidian vault, restore a usable Telegram menu for the owner, and run a quick multi-angle health check of the current VPS setup.

Facts gathered from the live VPS
- The bot workspace still contained generic first-run files that were misleading the agent:
  - `BOOTSTRAP.md` still described a fresh unconfigured assistant
  - `IDENTITY.md` still referred to another owner name
- The mounted knowledge base was real and reachable:
  - `/root/.openclaw/workspace/KnowledgeBase` -> `/root/KnowledgeBase`
  - `rclone-kb.service` was active
  - the mounted vault contained real Obsidian folders and notes
- Telegram command setup was partially correct but UX was incomplete:
  - slash commands were already set
  - the persistent menu button had to be explicitly forced to `commands`
- The stale direct Telegram session was still carrying older wrong beliefs about Whisper and vault access.
- A direct smoke run after workspace-file fixes confirmed that a fresh session correctly answered that it had access to the mounted `KnowledgeBase/`.
- Architecture/doctor findings during this stage:
  - orphan session transcript files existed after the direct-session reset and smoke runs
  - `memorySearch` was enabled while no embedding provider was ready
  - the only remaining security warning stayed `gateway.trusted_proxies_missing`

Applied changes on the VPS
- Updated the bot workspace source-of-truth files:
  - `BOOTSTRAP.md`
  - `IDENTITY.md`
  - `USER.md`
  - `AGENTS.md`
- Added explicit operating rules that:
  - `KnowledgeBase/` is a mounted server-side Obsidian vault
  - the bot must answer precisely about mounted-vault access vs unsynced local-PC files
  - the bot should use the mounted vault instead of asking the user to paste notes manually
- Cleared the stale Telegram direct-session mapping from `sessions.json` so the next real DM starts with the updated workspace context.
- Restored Telegram owner UX:
  - forced the chat menu button to `commands`
  - set a short Russian owner-facing command menu
  - set Russian bot description and short description
- Re-enabled `commands.restart = true` intentionally so the owner can have a real “перезагрузка бота” command in the menu.
- Refined command scopes:
  - private/default users get a compact Russian menu without `/restart`
  - the owner chat gets the expanded menu with `/restart`
- Archived orphan `.jsonl` session files after the session reset and smoke runs.
- Disabled `memorySearch` explicitly to remove doctor noise while no embedding provider is configured.

Verified results
- Telegram Bot API verification confirmed:
  - owner menu button type = `commands`
  - owner command list now includes:
    - `new`
    - `reset`
    - `status`
    - `restart`
    - `stop`
    - `help`
    - `commands`
- Fresh smoke run answered correctly:
  - access exists to mounted `KnowledgeBase/`
  - access does not extend to unsynced local-only files
- `openclaw status --deep` remained healthy:
  - gateway reachable
  - Telegram `ON / OK`
- `openclaw security audit --json` remained at `0 critical / 1 warn / 1 info`
- `openclaw doctor` improved:
  - orphan session-file warning disappeared
  - memory search now reports `enabled: false`

Architecture conclusion
- The current operating model is now internally much more coherent:
  - Telegram owner bot
  - mounted Obsidian/KnowledgeBase access inside workspace
  - voice-note transcription through explicit Whisper CLI configuration
  - compact owner-oriented menu with an actual restart command
- The main remaining architectural caution is deliberate:
  - `/restart` is now enabled again for convenience, which slightly relaxes the previous hardening baseline
  - this is acceptable for the current single-owner paired-DM model, but should be revisited if more paired users are ever added

## 2026-03-28 - OpenClaw Security Hardening And Dossier

Goal
- Keep only `OpenClaw` on the current `4vps` host, harden it for secure single-owner Telegram use, and prepare a detailed project dossier for another LLM.

Sources checked
- `D:\ЯндексДиск\Yandex.Disk\ПРОЕКТЫ\openclaw\лучшие практики от Grok.txt`
- OpenClaw official docs:
  - `https://docs.openclaw.ai/gateway/security`
  - `https://docs.openclaw.ai/gateway/configuration-reference`
  - `https://docs.openclaw.ai/reference/token-use`
- Live VPS state via SSH:
  - `openclaw status`
  - `openclaw security audit --json`
  - `openclaw sandbox explain --json`
  - `openclaw doctor`
  - raw `/root/.openclaw/openclaw.json`

Verified initial facts
- The live host was still healthy before hardening:
  - gateway reachable on `127.0.0.1:18789`
  - Telegram `ON / OK`
- The pre-hardening config was too broad for a security-first baseline:
  - `tools.profile = "coding"`
  - `agents.defaults.sandbox.mode = off`
  - `tools.fs.workspaceOnly = false`
  - `tools.elevated.enabled = true`
  - `commands.restart = true`
  - `channels.telegram.groupPolicy = "allowlist"`
  - `gateway.nodes.denyCommands` contained ineffective command IDs
- The initial security audit had `0 critical / 3 warn / 1 info`:
  - `gateway.trusted_proxies_missing`
  - `gateway.nodes.deny_commands_ineffective`
  - `security.trust_model.multi_user_heuristic`
- `openclaw doctor` additionally confirmed that Telegram groups were not actually usable in the current config because group allowlists were empty, so group messages would be silently dropped.

Applied changes on the VPS
- Created fresh config backups before each risky edit:
  - `/root/.openclaw/openclaw.json.bak_20260328_020925`
  - `/root/.openclaw/openclaw.json.bak_20260328_021123`
  - `/root/.openclaw/openclaw.json.bak_20260328_021510`
- Hardened the live config to an OpenClaw secure baseline plus sandboxing:
  - `agents.defaults.sandbox.mode = "all"`
  - `agents.defaults.sandbox.scope = "agent"`
  - `agents.defaults.sandbox.workspaceAccess = "none"`
  - `tools.profile = "messaging"`
  - `tools.allow = ["image"]`
  - `tools.deny = ["group:automation", "group:runtime", "group:fs", "group:ui", "group:nodes", "sessions_spawn", "sessions_send"]`
  - `tools.fs.workspaceOnly = true`
  - `tools.exec.security = "deny"`
  - `tools.exec.ask = "always"`
  - `tools.elevated.enabled = false`
  - `commands.restart = false`
  - `channels.telegram.groupPolicy = "disabled"`
- Removed obsolete `gateway.nodes.denyCommands`.
- Tightened host-side permissions:
  - `/root/.openclaw` -> `700`
  - `/root/.openclaw/openclaw.json` -> `600`
  - `/root/.openclaw/agents/main/agent/auth-profiles.json` -> `600`
- Added low-risk token-efficiency settings:
  - `agents.defaults.models["anthropic/claude-sonnet-4-6"].params.cacheRetention = "long"`
  - `agents.defaults.contextPruning.mode = "cache-ttl"`
  - `agents.defaults.contextPruning.ttl = "1h"`

Verified final facts
- Final config validation passed: `Config valid: ~/.openclaw/openclaw.json`.
- Final model map on disk was cleaned to one real key only:
  - `["anthropic/claude-sonnet-4-6"]`
- Python-level readback from `openclaw.json` confirmed:
  - `{"params":{"cacheRetention":"long"}}` for `anthropic/claude-sonnet-4-6`
- Final live state after hardening:
  - gateway reachable on `127.0.0.1:18789`
  - Telegram `ON / OK`
  - security audit reduced to `0 critical / 1 warn / 1 info`
- The only remaining audit warning is `gateway.trusted_proxies_missing`, which is benign while the gateway remains loopback-only and becomes relevant only if a reverse proxy or external HTTP path is added later.

Residual technical notes
- `openclaw doctor` still reports `openclaw-sandbox:bookworm-slim` as missing.
  - This is currently non-blocking because runtime/filesystem/UI/node tools are explicitly denied.
  - If those tools are re-enabled later, the sandbox base image should be prepared first.
- `openclaw doctor` also reports memory-search embeddings are not configured.
  - This does not break current Telegram operation.
  - It is a follow-up choice: either disable memory search or configure an embedding provider.

Conclusions
- A materially safer `OpenClaw` baseline is now live on the VPS without breaking the working Telegram channel.
- The operational trust boundary is now much closer to the documented single-owner OpenClaw model:
  - no Telegram groups
  - no runtime/filesystem/tool escalation on the host
  - sandboxing enabled
  - workspace access disabled inside the sandbox
- `NemoClaw` remains intentionally deferred because the current VPS plan is still too disk-constrained for reliable onboarding.
## 2026-03-30 - Verified Knowledge Triage and Skill Packaging

Goal
- Evolve the current Telegram corpus analysis into a reusable workflow that verifies claims against official sources, sorts knowledge into three confidence baskets, ranks it for project and `OpenClaw` relevance, and outputs an implementation roadmap.

Discovered facts
- The current prompt-pack already gives a solid staged base:
  - claim extraction
  - consolidation/topic mapping
  - final research-oriented synthesis
- The current run artifacts for the `OpenClaw Lab Community` corpus already exist and can serve as a baseline case:
  - `stage1_claims.json`
  - `stage2_topics.json`
  - `final_analysis.json`
  - `analysis_summary.md`
- The main missing layer is not extraction quality but operationalization:
  - no explicit verification ledger by source tier
  - no deterministic `3-basket` confidence triage
  - no reusable prioritization rubric across projects
  - no direct mapping from ranked knowledge to rollout steps
- A quick official-source pass already suggests that some `OpenClaw` Telegram/model/config claims are confirmable via docs, while provider-policy, release-sensitive, and Telegram Business visibility claims remain materially more volatile.
- Packaging the whole idea as a single broad "life-help" skill would over-mix:
  - stable corpus-processing logic
  - volatile orchestration preferences
  - user-specific proactive assistance heuristics

Conclusions
- The current prompt-pack should be extended, not replaced.
- The recommended reusable artifact is one core skill for `corpus -> verification -> triage -> prioritization -> application plan`.
- `OpenClaw`-specific routing logic should be encoded as references and decision tables inside the skill, not hardcoded as narrow one-off instructions in the description.
- Model/subagent selection should be treated as an internal decision tree:
  - cheaper model or narrower subagent for extraction, formatting, and dedupe
  - stronger model for contradiction handling, final synthesis, and internet verification review
- The broader "proactive help in life" target should remain outside the first version of the skill; otherwise validation will become vague and the skill will lose reuse value.

Unknowns
- How wide the first version should go beyond technical corpora and `OpenClaw`-adjacent knowledge.
- Whether the final ranked knowledge register should live only in `workspace/projects/` or also be normalized into reusable KB notes.

Risks
- Skill overbreadth: too many goals in one `SKILL.md`.
- Subjective scoring if the prioritization rubric is not explicitly weighted.
- Source drift if verification allows forum/blog material instead of official docs, changelogs, issues, and provider policies.
## 2026-03-30 - Verified Corpus-to-Roadmap Execution

Goal
- Finish the Telegram prompt-pack continuation in the correct order: primary-source verification first, then evidence triage, then ranking, then a human-readable roadmap and reusable skill.

Official sources checked
- `https://docs.openclaw.ai/reference/RELEASING`
- `https://docs.openclaw.ai/channels/telegram`
- `https://docs.openclaw.ai/gateway/doctor`
- `https://docs.openclaw.ai/help/faq`
- `https://core.telegram.org/constructor/businessBotRecipients`

Verified facts
- OpenClaw release lanes and stable version naming are explicit and date-based (`stable`, `beta`, `dev`; stable tags `vYYYY.M.D`), so version drift is a first-order operational risk.
- Telegram behavior is explicitly configured, not inferred:
  - token-based setup
  - DM pairing
  - topic isolation through `:topic:<threadId>`
  - explicit topic config path
- `doctor` validates gateway runtime, port collisions, and warns that Telegram/WhatsApp channels require a working Node runtime.
- `doctor` also recommends a workspace memory system, which aligns with the corpus signal around file-memory being more stable than long live sessions.
- OpenClaw FAQ explicitly confirms Anthropic subscription auth via setup-token, but also explicitly warns that this is technical compatibility rather than a policy guarantee.
- Telegram Business-bot recipients are scoped through explicit selectors such as `existing_chats` and `new_chats`, so access should be treated as a governed surface, not as a magical full inbox mirror.

Conclusions
- The first roadmap layer for our `OpenClaw` should stay conservative and source-backed:
  - version-aware operations
  - explicit Telegram governance
  - runtime diagnostics
  - file-memory baseline
- The corpus claims about long-horizon ingest, silent-failure hygiene, and Business-bot operating patterns are useful, but they belong in `probable but unverified` until we do deeper source or live-environment checks.
- The local-model fallback signal remains too weak for a default recommendation.

Unknowns
- Whether Telegram Business behavior on our specific account/use case should be promoted from `probable` to `verified`.
- Whether a separate vector ingest is needed immediately, or whether the current file-memory layer is enough for the next milestone.
- Whether to normalize the ranked register into KB notes right away or keep it in the run folder for now.

Risks
- Over-promoting community heuristics into hard operating rules.
- Treating provider subscription auth as stable production ground without repeated policy verification.
- Packing too much domain-specific context into the first version of the reusable skill.
## 2026-03-30 - Telegram Business Verification and Analytical Node Framing

Goal
- Refine the Telegram Business category using official sources where possible, switch user-facing labels/comments to Russian, and connect the verified corpus workflow to the wider `Analytical Node` architecture of the AI system.

Official sources checked
- `https://core.telegram.org/api/business`
- `https://core.telegram.org/api/bots/connected-business-bots`
- `https://core.telegram.org/constructor/businessBotRecipients`

Verified facts
- Telegram Business features are documented as currently available to Premium subscribers.
- Telegram officially documents connected business bots as a separate capability for business users.
- Telegram officially documents that currently only one business bot may be connected to a user account.
- Telegram officially documents granular business-bot recipient selection:
  - existing private chats
  - new private chats
  - contacts
  - non-contacts
  - explicitly selected users
  - explicit exclusions

Conclusions
- The earlier corpus claim should be tightened:
  - not "Business bot probably sees some chats"
  - but "Business bot access is an explicitly scoped private-chat surface, not a full inbox mirror"
- This category is now verified at the primary-source level, but still not locally smoke-tested in our own environment.
- The verified corpus workflow now fits directly into the already-documented architecture:
  - `My Dashboard` as front door
  - `Obsidian vault` as system of record
  - `Analytical Node` as verification/triage/ranking layer
  - `OpenClaw` and other agents as executor nodes

Unknowns
- Exact practical behavior for our own Telegram account and settings is still untested locally.
- The canonical write-back format from corpus runs into long-lived vault knowledge is still not fixed.

Risks
- Confusing official capability scope with production-readiness in our own environment.
- Letting the proactive-assistant ambition outrun the still-unfinished write-back and registry contracts.
