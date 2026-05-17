# PROTOCOL REGISTRY

last_review: 2026-05-17
next_review: 2026-08-17

## Antigravity AI System

### ACTIVE VERSIONS

| File | Version | Date | What Changed | Status |
| --- | --- | --- | --- | --- |
| AGENTS.md | v3.0.0 | 2026-03-22 | Full English rewrite, added intake protocol, interactive checkpoints, session hygiene signals, date-based T5, risk mapping, owner.md integration | ACTIVE |
| .agents/protocols/session-protocol.md | v2.0.0 | 2026-03-22 | English translation, added cross-project signal and handover storage convention | ACTIVE |
| .agents/templates/context-handover-template.md | v2.0.0 | 2026-03-22 | English translation, added protocol version and LLM model fields | ACTIVE |
| .agents/templates/adr-template.md | v2.0.0 | 2026-03-22 | English translation, added participants field | ACTIVE |
| .agents/steering/owner.md | v2.0.0 | 2026-03-22 | Activated (was wrapped in code block), English translation, added interactive preferences | ACTIVE |
| workspace/agents.md | v2.0.0 | 2026-03-22 | English translation, fixed corrupted runbook line | ACTIVE |

### SYSTEM SKILLS

| File | Version | Date | Status |
| --- | --- | --- | --- |
| .agents/skills/core-agent-rules/SKILL.md | v2.0.0 | 2026-03-22 | ACTIVE |
| .agents/skills/task-executor/SKILL.md | v1.1.0 | 2026-03-22 | ACTIVE |
| .agents/skills/safety-guardrails/SKILL.md | v1.0.0 | 2026-03-19 | ACTIVE |
| .agents/skills/version-control/SKILL.md | v1.0.0 | 2026-03-19 | ACTIVE |
| .agents/skills/skill-conductor/SKILL.md | v1.0.0 | 2026-03-19 | ACTIVE |

### DOMAIN SKILLS (not governed by core protocol — listed for completeness)

| File | Date | Status |
| --- | --- | --- |
| .agents/skills/advanced-rag-hybrid-search/SKILL.md | 2026-03-19 | ACTIVE |
| .agents/skills/docling-document-parsing/SKILL.md | 2026-03-19 | ACTIVE |
| .agents/skills/google-stitch-design/SKILL.md | 2026-03-25 | ACTIVE |
| .agents/skills/last-30-days-research/SKILL.md | 2026-03-19 | ACTIVE |
| .agents/skills/n8n-agentic-integration/SKILL.md | 2026-03-19 | ACTIVE |
| .agents/skills/vibe-coding-ui/SKILL.md | 2026-03-19 | ACTIVE |
| .agents/skills/youtube-monitoring/SKILL.md | 2026-03-19 | ACTIVE |
| .agents/skills/session-knowledge-harvester/SKILL.md | 2026-05-17 | ACTIVE |
| .agents/skills/nlm-skill/SKILL.md | 2026-05-17 | ACTIVE (migrated from global) |

### FIXED MODELS

| Role | Model | Model Version | Date Fixed |
| --- | --- | --- | --- |
| Orchestrator (Antigravity) | Claude | claude-sonnet-4-20250514 | 2026-03-22 |
| Coder / Alternate (Antigravity) | Gemini | gemini-2.5-pro | 2026-03-22 |
| Coder / Alternate (Antigravity) | Codex | codex (OpenAI) | 2026-03-22 |

Note: Antigravity supports multiple LLMs. The user switches between models per task. All models follow the same AGENTS.md protocol. The "Orchestrator" is whichever model runs the current session.

### VERSION HISTORY

#### v3.0.0 (2026-03-22)

Reason: Independent audit revealed 3 critical, 5 major, 6 minor issues. Full optimization sprint.
Changes:

- AGENTS.md: full English rewrite with all improvements
- owner.md: activated (was invisible to agents due to code block wrapper)
- workspace/agents.md: corrupted runbook line fixed, English translation
- Session protocol, handover template, ADR template: English + improvements
- core-agent-rules: added risk tier mapping and owner.md reference
- task-executor: added risk↔tier mapping note
- Created .agents/handovers/ directory
- Replaced session counter T5 with date-based review
- Registered all domain skills in registry
Test: manual verification of file links, rule consistency, and cross-file alignment
Rollback: use backups `AGENTS.md.backup_pre_optimization_2026-03-22`, `owner.md.backup`, `workspace/agents.md.backup`

#### v2.1.0 (2026-03-19)

Reason: protocol consolidation and registry launch
Changes: GUIDED/AUTONOMOUS mode, session-protocol.md, context-handover-template.md, adr-template.md, section 11 review triggers
Rollback: checkpoint `checkpoint_20260319_105850` or `AGENTS.md.backup_2026-03-20`

#### pre-registry baseline (2026-03-19)

Pre-refactoring AGENTS.md saved in `AGENTS.md.backup_2026-03-20`
