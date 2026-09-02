# External Audit Bundle

Generated: 2026-03-18T23:45:29+03:00

This archive is a curated, safer subset of the full system for an independent LLM audit.

Included:
- architecture notes
- implementation artifacts
- dashboard code and generated state
- selected brain notes relevant to system architecture and NotebookLM integration
- full file inventory and audit manifest
- redacted runtime config
- audit prompt

Not included directly:
- raw auth/cache state from C:\Users\Admin\.notebooklm-mcp-cli\
- full brain store
- unredacted secrets from mcp_config.json

Use 00_meta\external_llm_audit_prompt.md together with the manifest and inventory when sending this bundle to the external model.
