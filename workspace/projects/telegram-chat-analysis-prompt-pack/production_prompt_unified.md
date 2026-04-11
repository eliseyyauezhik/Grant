# Production Prompt — Unified Run

```text
Analyze the attached Telegram chat dataset about: [TOPIC].

Goal:
Transform the raw Telegram database into a structured analytical knowledge base that helps a human study the topic and use the information productively.

Tasks:
1. Extract meaningful claims from the dataset.
2. Merge semantically similar claims into consolidated claims without losing important differences.
3. Group them into topics and subtopics.
4. Rank them by:
   - current relevance,
   - chronology,
   - knowledge hierarchy (foundational -> operational -> specific -> edge cases).
5. Attach links to the relevant claims and topics.
6. Mark outdated, disputed, weak, and verification-needed items.
7. Build a source and evidence map.
8. Build an external research plan using high-quality web sources.
9. Build a step-by-step agent-tuning plan for [AGENT_TARGET].
10. The first step of the agent-tuning plan must always be: CREATE A BACKUP.
11. Prefer gradual, reversible changes and include verification and rollback for each step.

Rules:
- Treat chat data as a corpus of claims and evidence, not as automatic truth.
- Preserve chronology, contradictions, conditions, and links.
- Do not translate quotes, URLs, commands, filenames, or usernames.
- Write explanatory fields in Russian.

Return valid JSON only, matching the provided schema.
```
