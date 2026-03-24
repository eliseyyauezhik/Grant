# Handover: NotebookLM MCP Authentication Continuation

## Context

This project aims to bridge the `notebooklm-mcp` tools with the user's Google account. Configuration is complete, but authentication is currently stuck in an "expired" loop despite having fresh cookies.

## System Architecture

- **Environment**: Windows
- **MCP Config**: `C:\Users\Admin\.gemini\antigravity\mcp_config.json`
- **MCP Venv**: `C:\Users\Admin\.gemini\antigravity\venv\`
- **Storage Root**: `C:\Users\Admin\.notebooklm-mcp-cli\`

## Key Files & Storage

1. **`auth.json`**: Global cache used by MCP tools.
2. **`profiles/default/cookies.json`**: Profile-specific cookies used by the CLI (`nlm`).
3. **`profiles/default/metadata.json`**: Stores the `csrf_token`, `session_id`, and `build_label`.

## Current State

- `nlm doctor` reports valid status (Cookies: 24+, CSRF: present).
- `mcp_notebook_list` and `nlm list notebooks` return **"Authentication expired"**.
- This is a known issue caused by strict session binding (Fingerprinting) at `notebooklm.google.com`.

## How to Resume

1. **Force-Sync Strategy**: Use the script [update_auth.py](file:///C:/tmp/update_auth.py) (created during this session) to manually inject cookies.
2. **Missing Token**: If the error persists, you likely need the `at:` response header from a `batchexecute` request in the browser. This is the **real** CSRF token that Google expects in the POST body.
3. **Automation Opportunity**:
   - The CLI supports headless auth if the Chrome profile is warmed up.
   - Run `$env:PYTHONIOENCODING="utf-8"; nlm login --profile default` and wait for the browser to launch. The user can then login once, and the tokens should persist.

## Instructions for Next Agent

- **DO NOT** assume `mcp_save_auth_tokens` will work by itself; it currently fails to extract the CSRF token on Windows due to page structure changes.
- **DO** use the `Finalizing Authentication Build` TaskName if continuing this thread.
- **DO** check the `debug_page.html` in the storage root if extraction fails again.
