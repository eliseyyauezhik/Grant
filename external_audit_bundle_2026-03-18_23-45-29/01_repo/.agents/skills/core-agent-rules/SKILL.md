---
name: core-agent-rules
description: "Shared operational rules for context scan, workspace boundaries, approvals, artifact hygiene, and change safety across local skills. Use when creating, editing, or executing skills that touch files, commands, or external references in this workspace. Do NOT use for domain-specific task logic or tool-specific workflows."
---

# Core Agent Rules

## Overview
Apply this skill as the shared policy layer before repo-affecting work. Keep generic workspace rules here so task-specific skills can stay focused on their own execution logic.

## Shared Policy

1. Inspect relevant local files before proposing or making changes.
2. Read `AGENTS.md` and only the skill files needed for the current task.
3. Modify only the current workspace and harness-provided writable roots.
4. Treat edits outside writable roots, destructive actions, deploys, commits, and side-effecting external calls as approval-required.
5. Use sandboxed commands first. Request escalation only after a real sandbox or network blocker.
6. Reuse `research_notes.md`, `implementation_plan.md`, `task.md`, and `progress.md` instead of creating duplicates.
7. If a workflow artifact already contains another task, append a dated section instead of overwriting it.
8. Inspect dirty files before editing. Never revert unrelated user changes.
9. Create a checkpoint before risky edits, broad replacements, or changes to agent-system files such as `AGENTS.md` and `.agents/skills/**`.
10. Keep diffs small, reversible, and explicitly verified.
11. Log Tier 2 and Tier 3 actions to `agent_audit.log`.

## Common Mistakes
- Starting from assumptions instead of file context. Fix: inspect the repository first.
- Writing outside writable roots. Fix: treat it as approval-required.
- Overwriting shared workflow artifacts. Fix: append a dated section.
- Rolling back mixed user and agent changes. Fix: checkpoint first and inspect dirty state before revert.
