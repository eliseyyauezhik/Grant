# Session Protocol

This file describes context compaction rules, session-switch criteria, and handover discipline.

## 1. Core Principles

- Follow the rule `one task = one context` whenever possible.
- Use minimum viable context: only the files, dependencies, constraints, and artifacts actually needed.
- After each logically complete block, record a compact handover, even if continuing work in the same session.

## 2. Periodic Context Check (Proactive)

The agent performs a lightweight self-check at the following intervals, **without waiting for user signal**:

### 2.1 Check Interval Rules

| Session type | Check every | Criterion |
|---|---|---|
| **Mixed topics** (different projects/areas in one session) | **10–15 exchanges** | Topics diverge → higher drift risk |
| **Single topic** (one task, one project throughout) | **20–30 exchanges** | Context stays coherent longer |

### 2.2 Check Algorithm (3 questions)

At the checkpoint, the agent asks itself:

1. **Same task as before?**
   - Yes → continue, no action needed
2. **Important conclusions/decisions accumulated?**
   - Yes → briefly record in `owner.md` → Current State block
3. **Context drifting OR topic changed?**
   - Yes → propose a handover + switch to a new chat

> The agent signals the check to the user only if action is needed (points 2 or 3). Silent checks do not interrupt the flow.

## 3. When Context Compaction Is Needed (Reactive)

Trigger compaction if at least one signal is observed:

- Chat has exceeded approximately `40–50` exchanges;
- Responses are becoming longer but less specific;
- Constraints from the start of the session are being forgotten;
- The next step changes the module, layer, work type, or task domain;
- The user explicitly asks to stop the stage and continue later.

## 3. When to Switch Sessions

A switch to a new chat is mandatory if:

- The user explicitly ends the stage;
- Context has degraded to a level dangerous for quality;
- The next step changes the module, work type, or requires a clean context;
- The user's request concerns a **different project** (signal this to the user per AGENTS.md § 9.2).

If none of these conditions hold, the agent may continue in the same session after recording a handover.

## 4. What a Handover Must Contain

A handover must include:

- The task of the current session;
- Decisions made that should not be reconsidered without cause;
- What was implemented and verified;
- Current state;
- Next step;
- Risks, constraints, and "do not touch" items;
- Key files and artifacts;
- Protocol version (AGENTS.md version used during this session).

Use the template from [`context-handover-template`](../templates/context-handover-template.md).
Store handover files in `.agents/handovers/` with naming: `handover_YYYY-MM-DD_<topic>.md`.
