---
name: task-executor
description: Standard workflow for receiving, planning, executing and verifying any task. Use when user gives a task, request, or idea to implement. Do NOT use for simple Q&A or casual conversation.
---

# Task Executor

Standard operating procedure for handling any non-trivial task in this repository.

## Overview

Every non-trivial task follows the same pipeline: context scan, research, planning, execution, verification, reporting.
Default autonomy: proceed after a concise plan for low-risk work inside the current workspace. Ask for confirmation only for HIGH-risk, destructive, cross-project, deploy/commit, or major architectural changes.
Apply `core-agent-rules` first for shared workspace policy. This skill defines the task lifecycle, not the full global safety baseline.

**⚠️ IMPORTANT: Available Tools**
Before planning or executing tasks that require specific Python packages, external software, or frameworks, ALWAYS check the global tools list at:
`d:\ЯндексДиск\Yandex.Disk\ПРОЕКТЫ\AI_Workspace\KnowledgeBase\available_tools.md`
Use the tools listed there instead of blindly trying to install new ones or searching the web. If the repository contains a more specific local instruction, prefer the local instruction.

## Step 0: Context Scan

Before planning or editing:

1. Load `core-agent-rules`.
2. Inspect the relevant files and existing workflow artifacts for the current task.
3. Identify whether the work is LOW, MEDIUM, or HIGH risk before planning.

## Step 1: Receive and Parse

Extract from user request:

1. **Goal** — what is the desired end state? (1 sentence)
2. **Scope** — what files/systems are affected?
3. **Constraints** — deadlines, tech stack, budget limits?
4. **Success criteria** — how do we know it's done?

If any of the above are unclear and a wrong assumption would be costly, ask **one** clarifying question. Do not ask more than two questions total before starting.

Template:

```
Goal: [extracted goal]
Scope: [files/systems]
Constraints: [any limits]
Success: [how to verify]
```

## Step 2: Research

Before implementation:

1. Analyze edge cases, constraints, security implications, and current repository state.
2. Inspect existing diffs if they touch the same files.
3. Record concise findings in `research_notes.md`.

## Step 3: Plan

Decompose the goal into concrete steps:

1. List 3-10 numbered steps
2. For each step, estimate risk: LOW / MEDIUM / HIGH
3. HIGH risk steps require user confirmation before execution
4. Identify dependencies between steps
5. Define how each step will be verified

Template:

```
Plan:
1. [step] — risk: LOW
2. [step] — risk: LOW
3. [step] — risk: HIGH → needs confirmation
```

Persist the plan in `implementation_plan.md` and turn it into checkboxes in `task.md`.
Present the plan to the user and wait for approval when the work is HIGH risk, ambiguous, spans multiple systems, or the user explicitly asks for a plan/review.

## Step 4: Execute

For each approved or low-risk step:

1. Execute the step
2. Log the result (success/failure)
3. If failure → attempt recovery (max 2 retries)
4. If still failing → stop and report to user

Rules:

- Check `safety-guardrails` skill before any destructive action
- Follow `core-agent-rules` for approvals, checkpoint use, audit logging, writable roots, and shared artifact hygiene
- Update `task.md` as steps are completed

## Step 5: Verify

After all steps complete:

1. Re-read the success criteria from Step 1
2. Run any automated tests if applicable
3. For docs/config changes, check paths, references, syntax, and internal consistency
4. Check the output manually when automation is insufficient
5. If verification fails → return to Step 4 for the failing part

## Step 6: Report

Send results to the user.

**Text Report Format:**

1. Summary: what was done (2-3 sentences)
2. Files changed: list with links
3. Verification: what was checked and what could not be checked
4. Issues found: any problems, risks, or assumptions
5. What to check: specific things for user to verify if needed

## Optional Step 7: Self-Evaluate

If the repository already uses `critic_evaluations.csv`, append a brief self-evaluation after the task is complete. If the file does not exist, skip this step.

Suggested axes:
- **Clarity**
- **Efficiency**
- **Quality**
- **Safety**
- **Communication**

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Starting without inspecting the repo | Always complete Step 0 first |
| Asking too many questions | Max 2 questions, then start |
| Overwriting shared artifacts | Append dated sections when notes already contain another task |
| Not checking safety before file ops | Always consult safety-guardrails |
| Forgetting to verify | Step 5 is mandatory, never skip |
| Not reporting the result | Step 6 is mandatory |

## Troubleshooting

Error: Task too vague → Ask: "What does 'done' look like for you?"
Error: Step fails twice → Stop, report, ask user how to proceed.
Error: Multiple tasks in one request → Split into separate executions, do them sequentially.
