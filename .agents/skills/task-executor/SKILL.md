---
name: task-executor
description: Standard workflow for receiving, planning, executing and verifying any task. Use when user gives a task, request, or idea to implement. Do NOT use for simple Q&A or casual conversation.
---

# Task Executor

Standard operating procedure for handling any task — from idea to verified result.

## Overview

Every non-trivial task follows the same 6-step pipeline. This skill ensures consistent quality and reduces improvisation. Uses autonomy level B: plan autonomously, ask confirmation before execution.

## Step 1: Receive and Parse

Extract from user request:

1. **Goal** — what is the desired end state? (1 sentence)
2. **Scope** — what files/systems are affected?
3. **Constraints** — deadlines, tech stack, budget limits?
4. **Success criteria** — how do we know it's done?

If any of the above are unclear, ask **one** clarifying question. Do not ask more than two questions total before starting.

Template:

```
Goal: [extracted goal]
Scope: [files/systems]
Constraints: [any limits]
Success: [how to verify]
```

## Step 2: Plan

Decompose the goal into concrete steps:

1. List 3-10 numbered steps
2. For each step, estimate risk: LOW / MEDIUM / HIGH
3. HIGH risk steps require user confirmation before execution
4. Identify dependencies between steps

Template:

```
Plan:
1. [step] — risk: LOW
2. [step] — risk: LOW  
3. [step] — risk: HIGH → needs confirmation
```

Present the plan to the user. Wait for approval (autonomy B).

## Step 3: Execute

For each approved step:

1. Execute the step
2. Log the result (success/failure)
3. If failure → attempt recovery (max 2 retries)
4. If still failing → stop and report to user

**Voice Interaction (if user spoke to you):**

- For HIGH risk steps that need confirmation, send a short voice message: "План готов, ожидаю вашего подтверждения в чате."
- Use `send-voice-message.md` workflow for this.

Rules:

- Check `safety-guardrails` skill before any destructive action
- Create files in the project working directory, never in system dirs
- Commit checkpoint after each major step (update task.md)

## Step 4: Verify

After all steps complete:

1. Re-read the success criteria from Step 1
2. Run any automated tests if applicable
3. Check the output manually (open files, screenshot, etc.)
4. If verification fails → return to Step 3 for the failing part

## Step 5: Report

Send results to the user:

**Channel Selection:**

- If the user wrote text → reply with text.
- If the user sent a Voice Message → send a text summary AND a short voice summary (using `send-voice-message.md`).
- Voice summary should be short, max 2-3 sentences, without Markdown or code.

**Text Report Format:**

1. Summary: what was done (2-3 sentences)
2. Files changed: list with links
3. What to check: specific things for user to verify
4. Issues found: any problems or concerns

## Step 6: Self-Evaluate

After the task is complete:

1. Rate own performance on 5 axes (1-10):
   - **Clarity** — did I understand the task correctly?
   - **Efficiency** — did I use minimal steps?
   - **Quality** — is the output correct and complete?
   - **Safety** — did I avoid risky actions?
   - **Communication** — did I keep the user informed?
2. Log the evaluation to `critic_evaluations.csv`
3. If any axis < 6, note the specific improvement needed

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Starting without understanding the goal | Always complete Step 1 first |
| Asking too many questions | Max 2 questions, then start |
| Not checking safety before file ops | Always consult safety-guardrails |
| Forgetting to verify | Step 4 is mandatory, never skip |
| Not reporting the result | Step 5 is mandatory |

## Troubleshooting

Error: Task too vague → Ask: "What does 'done' look like for you?"
Error: Step fails twice → Stop, report, ask user how to proceed.
Error: Multiple tasks in one request → Split into separate executions, do them sequentially.
