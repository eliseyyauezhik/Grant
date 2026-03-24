---
name: core-agent-rules
description: "Shared operational rules for context scan, workspace boundaries, approvals, artifact hygiene, and change safety across local skills. Use when creating, editing, or executing skills that touch files, commands, or external references in this workspace. Do NOT use for domain-specific task logic or tool-specific workflows."
---

# Core Agent Rules

## Overview

Apply this skill as the shared policy layer before repo-affecting work. Keep generic workspace rules here so task-specific skills can stay focused on their own execution logic.

**This skill is a convenience summary. The authoritative source of truth is `AGENTS.md`.** If any rule here conflicts with `AGENTS.md`, `AGENTS.md` wins.

## Shared Policy

1. Inspect relevant local files before proposing or making changes.
2. Read `AGENTS.md` and only the skill files needed for the current task.
3. Read `.agents/steering/owner.md` to understand owner context and preferences.
4. Modify only the current workspace and harness-provided writable roots.
5. Treat edits outside writable roots, destructive actions, deploys, commits, and side-effecting external calls as approval-required.
6. Use sandboxed commands first. Request escalation only after a real sandbox or network blocker.
7. Reuse `research_notes.md`, `implementation_plan.md`, `task.md`, and `progress.md` instead of creating duplicates.
8. If a workflow artifact already contains another task, append a dated section instead of overwriting it.
9. Inspect dirty files before editing. Never revert unrelated user changes.
10. Create a checkpoint before risky edits, broad replacements, or changes to agent-system files such as `AGENTS.md` and `.agents/skills/**`.
11. Keep diffs small, reversible, and explicitly verified.
12. Log Tier 2 and Tier 3 actions to `agent_audit.log`.

## Risk Tier Mapping

When `task-executor` classifies a task step as LOW / MEDIUM / HIGH risk, the following mapping to `safety-guardrails` tiers applies:

| Task Risk | Safety Tier | Confirmation Required? |
|---|---|---|
| LOW | Tier 1–2 | No (Tier 2 is logged) |
| MEDIUM | Tier 2 | No, but logged |
| HIGH | Tier 3 | Yes — explicit user approval |

Always check `safety-guardrails` before each concrete action, regardless of the overall task risk level.

## Common Mistakes

- Starting from assumptions instead of file context. Fix: inspect the repository first.
- Writing outside writable roots. Fix: treat it as approval-required.
- Overwriting shared workflow artifacts. Fix: append a dated section.
- Rolling back mixed user and agent changes. Fix: checkpoint first and inspect dirty state before revert.
- Ignoring owner profile. Fix: read `.agents/steering/owner.md` at session start.
