---
name: verified-corpus-roadmap
description: Turn a Telegram export, chat archive, or database corpus into a verified knowledge register and implementation roadmap. Use when corpus claims must be checked against primary sources, triaged into evidence buckets, ranked for practical value, and converted into concrete project actions. Do NOT use for casual summarization, one-off web research without a corpus, or broad life-orchestration requests.
---

# Verified Corpus Roadmap

## Overview

Convert corpus analysis into something operational: verified knowledge, ranked priorities, and a rollout plan. Reuse existing structured outputs when available instead of re-extracting the same claims.

## Workflow

1. Confirm the corpus and the desired decision target.
   - Example targets: `OpenClaw` roadmap, Telegram operating policy, provider strategy, KB migration priorities.
2. Reuse existing structured artifacts first.
   - Prefer `stage1_claims.json`, `stage2_topics.json`, `final_analysis.json`, or similar run outputs if they already exist.
3. Build a verification ledger before ranking.
   - Check primary sources first: official docs, specs, release notes, official issues, provider policy pages.
   - Mark what is verified, what is only probable, and what is volatile.
4. Apply the evidence model and scoring rubric from `references/evidence-model.md`.
5. Produce the outputs from `references/output-contract.md`.
6. Only after the ranked register is stable, derive roadmap phases and project actions.
7. If the user also wants reuse, package the workflow or findings into a local skill, KB note, or playbook.

## Routing

- Use a cheaper model or narrower subagent for extraction, dedupe, formatting, and table cleanup.
- Use a stronger model for contradiction handling, official-source review, and final synthesis.
- Browse the internet for time-sensitive claims. Do not rank volatile product or policy claims from memory.

## Output Rules

- Rank only after verification.
- Do not let chat/forum sources overrule official docs.
- Keep time-sensitive claims separate from stable operating rules.
- Always produce a human-readable Markdown output, not only JSON.
- If the user wants a "convenient library view", organize findings as:
  - verified
  - useful but unverified
  - experimental or volatile
  - roadmap phases

## Common Mistakes

- Turning the task into a generic summary instead of a decision artifact.
- Mixing verified facts with community guesses in one bucket.
- Ranking claims before checking primary sources.
- Over-expanding into vague "life orchestration" instead of a narrow corpus-to-roadmap workflow.
