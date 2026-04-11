# Handover — Verified Corpus Roadmap

## Task

Continue the Telegram prompt-pack work by adding a primary-source verification pass, a reusable ranking framework, a human-readable `OpenClaw` trajectory document, and a narrow reusable skill for `corpus -> verification -> triage -> prioritization -> roadmap`.

## Inputs

- `workspace/projects/telegram-chat-analysis-prompt-pack/`
- `workspace/projects/telegram-chat-analysis-prompt-pack/runs/2026-03-29_openclaw-lab-community/`
- existing workflow artifacts: `research_notes.md`, `implementation_plan.md`, `task.md`, `progress.md`
- official sources checked on `2026-03-30`

## New Outputs

- `workspace/projects/telegram-chat-analysis-prompt-pack/verified_corpus_to_roadmap_framework.md`
- `workspace/projects/telegram-chat-analysis-prompt-pack/runs/2026-03-29_openclaw-lab-community/verified_knowledge_roadmap.md`
- `.agents/skills/verified-corpus-roadmap/`

## Key Conclusions

- The correct order is `verify -> bucket -> rank -> roadmap`, not `summarize -> rank`.
- The strongest verified priorities for `OpenClaw` are:
  - version-aware operations
  - explicit Telegram channel/topic/ACL design
  - runtime-first diagnostics
  - file-memory baseline
- Anthropic subscription auth is technically supported but explicitly policy-sensitive.
- Long-horizon corpus ingest and silent-failure hygiene look valuable, but are still one layer less certain than the verified operational baseline.

## Verification Done

- Checked official OpenClaw docs for release policy, Telegram behavior, doctor/runtime guidance, and Anthropic auth guidance.
- Checked official Telegram API schema for Business-bot recipient scope.
- Created a reusable scoring/ranking framework and applied it to the current corpus.
- Added a reusable local skill and validated it with local skill-conductor tooling.

## Remaining Follow-Up

1. If needed, normalize the ranked register into KB notes instead of keeping it only in the run folder.
2. If needed, run a live Telegram Business-bot test to move that area from `probable` to `verified` or `rejected`.
3. If needed, extend the new skill with domain-specific references for non-OpenClaw corpora.
