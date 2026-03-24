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
