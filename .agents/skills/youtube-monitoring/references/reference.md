# Reference Documentation for Youtube Monitoring

## Report JSON shape

```json
{
  "report_id": "YT_Report_YYYYMMDD_HHMMSS",
  "generated_at": "ISO-8601",
  "source_url": "https://...",
  "criteria": "topic1, topic2",
  "total_videos": 15,
  "high_relevance_count": 7,
  "average_score": 72.3,
  "top_videos": [
    {
      "video_id": "abc123",
      "title": "...",
      "url": "https://...",
      "relevance_score": 95,
      "relevance_reason": "...",
      "categories": ["topic1"],
      "key_insights": ["..."],
      "actionable_ideas": ["..."],
      "trends": ["..."],
      "summary": "...",
      "mindmap": {"root": "...", "branches": {}}
    }
  ],
  "all_trends": ["..."],
  "all_insights": ["..."],
  "errors": [],
  "elapsed_seconds": 12.3,
  "run_id": "YYYYMMDD_HHMMSS"
}
```

## Knowledge base file

- Path: `scripts/knowledge_base/knowledge_base.json`
- Fields: videos map, trends list, insights list, last_updated

## Provider configuration

- Gemini (default):
- `LLM_PROVIDER=gemini`
- `GEMINI_API_KEY=...` or `GOOGLE_API_KEY=...`
- `GEMINI_MODEL=gemini-2.5-pro` (optional)

- Anthropic:
- `LLM_PROVIDER=anthropic`
- `ANTHROPIC_API_KEY=...`
- `ANTHROPIC_MODEL=claude-opus-4-6` (optional)
