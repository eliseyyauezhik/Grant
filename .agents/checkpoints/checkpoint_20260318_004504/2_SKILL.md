---
name: safety-guardrails
description: Safety rules and boundaries for autonomous agent execution. Use when performing any file system operation, API call, or system change. Do NOT use for read-only queries or conversation.
---

# Safety Guardrails

Hard safety boundaries for autonomous agent operation. Domain Intelligence pattern — compliance before action.

## Overview

All agent actions pass through this pre-check. Actions are classified into three tiers. Tier 1 is always allowed, Tier 2 requires logging, Tier 3 requires explicit user confirmation.

## Pre-Check: Action Classification

Before ANY action, classify it:

### Tier 1: Always Allowed (no confirmation needed)

- Read files in the current workspace
- Read external reference files that are directly relevant to the current task
- Search the web (Tavily, built-in search)
- Generate text, plans, summaries
- Create new files in project working directories
- Take screenshots
- Analyze code or data
- Log actions to audit trail

### Tier 2: Allowed with Logging (no confirmation, but logged)

- Edit existing files inside the current workspace or other writable roots
- Create checkpoints or roll back through `.agents/checkpoints`
- Install Python packages in a project-local virtual environment
- Run safe terminal commands (`rg`, `git status`, tests, formatters, local scripts)
- Make read-only GET requests to external APIs when the task requires it
- Update project journals such as `agent_audit.log`, `research_notes.md`, `implementation_plan.md`, `task.md`

### Tier 3: Requires User Confirmation

- **Delete** any file or directory
- **Edit or overwrite** files outside the current workspace or writable roots
- Execute commands that modify system state (registry, services)
- POST/PUT/DELETE requests to external APIs with side effects
- Any action involving money (API billing, purchases)
- Sharing credentials or sensitive data externally
- Running unknown or downloaded executables
- Modifying system PATH or environment variables globally
- Git push, force push, branch delete
- Broad overwrite of many files when the user did not explicitly request it

## Execution Rules

1. **Project boundaries.** Only modify files within:
   - `d:\ЯндексДиск\Yandex.Disk\ПРОЕКТЫ\Грант для гимназии Давыдова\Инженерный грант\`
   - Other writable roots explicitly provided by the harness
   - Project-local temp or checkpoint directories

   Read-only reference locations allowed when relevant:
   - `D:\ЯндексДиск\Yandex.Disk\ПРОЕКТЫ\KnowledgeBase\`
   - `d:\ЯндексДиск\Yandex.Disk\ПРОЕКТЫ\AI_Workspace\KnowledgeBase\`
   - Skill directories referenced by `AGENTS.md`

2. **Sandbox first.** Run commands inside the sandbox first. If a required command fails because of sandbox restrictions or network limitations, request escalation with a short, task-specific justification.

3. **Dirty-state awareness.** Before editing, check whether target files already contain user changes. Never revert unrelated work. If unexpected changes affect the current task, adapt to them and mention this in the final report.

4. **Sensitive system files.** Changes to `AGENTS.md`, `.agents/skills/**`, audit logs, or workflow artifacts require:
   - a checkpoint before editing
   - a concise rationale in the final report
   - Tier 2 logging

5. **Timeout.** If any single operation takes longer than 60 seconds, abort and report.

6. **Error escalation.** If an action fails twice:
   - Do NOT retry a third time
   - Report the error to the user
   - Suggest alternative approaches

7. **No credential exposure.** Never include API keys, tokens, or passwords in:
   - Chat messages
   - Log files accessible externally
   - Generated content or reports
   Exception: config files that already contain them (e.g., config.json)

## Audit Trail

Log every Tier 2 and Tier 3 action to `agent_audit.log` in UTF-8:

```
[TIMESTAMP] [TIER] [ACTION] [TARGET] [RESULT]
```

Example:

```
[2026-03-17 23:20:00] [T2] CHECKPOINT d:\repo\AGENTS.md SUCCESS
[2026-03-17 23:21:00] [T2] EDIT d:\repo\.agents\skills\task-executor\SKILL.md SUCCESS
[2026-03-17 23:22:00] [T3] DELETE d:\repo\old.md BLOCKED:NEEDS_CONFIRMATION
```

Recommended action labels:
- `READ_EXTERNAL`
- `CHECKPOINT`
- `EDIT`
- `CMD`
- `VERIFY`
- `BLOCKED`

## Common Mistakes

| Mistake | Rule |
|---------|------|
| Deleting without asking | ALWAYS ask for Tier 3 |
| Editing outside writable roots | Treat it as Tier 3 and request approval |
| Running pip install globally | Use project venv only |
| Sending API keys in messages | Never expose credentials |
| Infinite retry loops | Max 2 retries, then escalate |
| Modifying files outside project | Check project boundaries first |

## Emergency Stop

If the agent detects it is in an undefined or potentially harmful state:

1. Stop all actions immediately
2. Log the state
3. Report to user with full context
4. Wait for explicit instructions
