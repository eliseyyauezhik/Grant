# Runtime Exclusions And Redactions

This bundle intentionally excludes raw runtime secrets and auth state.

Excluded from the archive but present in the full inventory:
- `C:\Users\Admin\.notebooklm-mcp-cli\` (auth/cache/profile runtime state)
- most of `C:\Users\Admin\.gemini\antigravity\brain\` except selected audit-relevant notes
- live secrets from `C:\Users\Admin\.gemini\antigravity\mcp_config.json`

Included instead:
- redacted `mcp_config.redacted.json`
- full absolute-path inventory for follow-up targeted requests
- manifest describing sensitivity zones
