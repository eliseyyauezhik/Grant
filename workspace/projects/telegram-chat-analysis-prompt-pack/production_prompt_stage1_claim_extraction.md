# Production Prompt — Stage 1 Claim Extraction

```text
Analyze the attached Telegram chat dataset about: [TOPIC].

Stage objective:
Extract meaningful claims and related evidence from the source database.

Tasks:
1. Identify meaningful claims, recommendations, decisions, problems, solutions, observations, dependencies, warnings, hypotheses, and unresolved questions.
2. Preserve variants instead of merging them too early.
3. Attach message references, dates, speakers (if available), and links.
4. Assign an initial topic candidate and subtopic candidate.
5. Assess preliminary confidence and source reliability.
6. Mark claims that require external verification.

Rules:
- Do not treat repetition as fact.
- Preserve original wording in quotes and links.
- Keep Russian source text in original form.
- Write explanatory fields in Russian.

Return valid JSON only, matching the provided Stage 1 schema.
```
