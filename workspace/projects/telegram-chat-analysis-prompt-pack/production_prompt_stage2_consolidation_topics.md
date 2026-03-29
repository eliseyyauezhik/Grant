# Production Prompt — Stage 2 Consolidation and Topic Clustering

```text
Using the previously extracted claims and, if needed, the source dataset again, perform consolidation and topic clustering for: [TOPIC].

Stage objective:
Turn the raw claim inventory into a coherent topic map with consolidated claims.

Tasks:
1. Merge semantically similar claims into consolidated claims.
2. Preserve important differences, conditions, chronology, and conflicts.
3. Build topics and subtopics.
4. Rank content inside each topic:
   - current core first,
   - historical versions later,
   - foundational before operational,
   - exceptions and edge cases at the end.
5. Keep links attached to the relevant consolidated claims and topics.
6. Mark disputed and weakly supported items explicitly.
7. Highlight rare but high-signal items.

Rules:
- Do not over-merge.
- Do not silently resolve contradictions.
- Preserve original links and quotations.
- Write explanatory fields in Russian.

Return valid JSON only, matching the provided Stage 2 schema.
```
