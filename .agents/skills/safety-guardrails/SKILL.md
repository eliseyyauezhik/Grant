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

- Read files in project directories
- Search the web (Tavily, built-in search)
- Generate text, plans, summaries
- Create new files in project working directories
- Take screenshots
- Analyze code or data
- Log actions to audit trail

### Tier 2: Allowed with Logging (no confirmation, but logged)

- Edit existing files (with backup awareness)
- Install Python packages in virtual environment
- Run safe terminal commands (ls, cat, grep, git status)
- Send messages to user via Telegram
- Make GET requests to external APIs

### Tier 3: Requires User Confirmation

- **Delete** any file or directory
- **Overwrite** files outside the project directory
- Execute commands that modify system state (registry, services)
- POST/PUT/DELETE requests to external APIs with side effects
- Any action involving money (API billing, purchases)
- Sharing credentials or sensitive data externally
- Running unknown or downloaded executables
- Modifying system PATH or environment variables globally
- Git push, force push, branch delete

## Execution Rules

1. **Project boundaries.** Only modify files within:
   - `F:\ДИМА\ПРОЕКТЫ\ИИ агент на компьютер\` (main project)
   - `C:\Users\Admin\.copaw\` (CoPaw config)
   - `C:\Users\Admin\.gemini\` (Antigravity artifacts)
   - Temp directories for scratch files

2. **API rate limits.** Maximum per session:
   - Gemini API: 50 calls
   - Tavily API: 20 calls
   - Telegram API: 10 messages
   - If approaching limit, warn user before continuing

3. **Timeout.** If any single operation takes longer than 60 seconds, abort and report.

4. **Error escalation.** If an action fails twice:
   - Do NOT retry a third time
   - Report the error to the user
   - Suggest alternative approaches

5. **No credential exposure.** Never include API keys, tokens, or passwords in:
   - Chat messages
   - Log files accessible externally
   - Generated content or reports
   Exception: config files that already contain them (e.g., config.json)

## Audit Trail

Log every Tier 2 and Tier 3 action to `agent_audit.log`:

```
[TIMESTAMP] [TIER] [ACTION] [TARGET] [RESULT]
```

Example:

```
[2026-03-04 10:30:00] [T2] EDIT F:\project\main.py SUCCESS
[2026-03-04 10:31:00] [T3] DELETE F:\project\old.py BLOCKED:NEEDS_CONFIRMATION
```

## Common Mistakes

| Mistake | Rule |
|---------|------|
| Deleting without asking | ALWAYS ask for Tier 3 |
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
