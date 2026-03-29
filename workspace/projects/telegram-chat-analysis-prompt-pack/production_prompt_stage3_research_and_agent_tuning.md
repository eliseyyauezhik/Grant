# Production Prompt — Stage 3 Research and Agent Tuning

```text
Using the consolidated claims and topic map for: [TOPIC], create the final analytical layer.

Stage objective:
Produce a source-aware external research plan and a safe, step-by-step agent-tuning brief for [AGENT_TARGET].

Tasks:
1. Identify which claims and topics require external verification.
2. Build an external research roadmap, prioritizing:
   - official documentation,
   - primary sources,
   - standards/specs/papers,
   - official blogs,
   - specialist publications,
   - expert analyses,
   - forums only as supplementary material.
3. Produce a step-by-step tuning brief for another model.
4. The first implementation step must always be: CREATE A BACKUP.
5. Separate:
   - stable rules,
   - supported working knowledge,
   - hypotheses,
   - unresolved questions.
6. For each tuning step include:
   - goal,
   - input from analysis,
   - exact change,
   - backup procedure,
   - verification,
   - risk,
   - rollback.
7. Produce a practical knowledge set: short, useful, sufficiently supported formulations.

Rules:
- No irreversible recommendation without backup.
- Preserve provenance and uncertainty.
- Write explanatory fields in Russian.

Return valid JSON only, matching the provided final schema.
```
