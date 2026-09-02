# NotebookLM MCP Configuration and Authentication Fix

The goal is to ensure `notebooklm-mcp` is correctly configured in `mcp_config.json` and that authentication is valid, allowing the use of MCP tools like `notebook_list`.

## User Review Required

> [!IMPORTANT]
> Authentication is currently failing with "expired" status despite having tokens present.
> You may need to run `nlm login` manually in a terminal to refresh the session if the current `temp_cookies.txt` are indeed expired.

## Proposed Changes

### [Component Name] Configuration

#### [MODIFY] [mcp_config.json](file:///C:/Users/Admin/.gemini/antigravity/mcp_config.json)

- Verify the current entry is correct.
- If the user prefers a different python environment (e.g., the global one), I will update the `command` path.

### [Component Name] Authentication

- Use `mcp_save_auth_tokens` to import fresh cookies if the user provides them.
- Provide a guide on how to get fresh cookies.

## Verification Plan

### Automated Tests

- Run `mcp_notebook_list` to verify successful connection.
- Run `nlm doctor` to check the tool's internal health status.

### Manual Verification

- Ask the user to try running a query through the notebook tool to ensure end-to-end functionality.
