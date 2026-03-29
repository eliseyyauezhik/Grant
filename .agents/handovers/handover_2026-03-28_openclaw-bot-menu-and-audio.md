## HANDOVER: OpenClaw bot menu and audio cleanup — 2026-03-28

### 1. SESSION TASK

Continue the latest OpenClaw VPS handover autonomously: verify the real live state, fix the outdated Telegram slash-command menu, and clean up the legacy audio config without breaking the working bot.

### 2. DECISIONS MADE

- Did not trust the earlier assumption that the daemon was down; re-checked the live VPS first.
- Kept the working hardened OpenClaw baseline instead of reopening broader capabilities.
- Replaced the stale legacy `plugins.entries.audio` config with the current documented `tools.media.audio` block.
- Published only slash commands that are actually supported by the current OpenClaw build.
- Intentionally did not publish `/resume` because it does not appear in the current supported `getMyCommands` output.

### 3. IMPLEMENTED AND VERIFIED

- Live checks confirmed before the fix:
  - gateway reachable on `127.0.0.1:18789`
  - Telegram `ON / OK`
  - `getMyCommands` still returned the long default English menu
  - `openclaw status` showed `plugins.entries.audio: plugin not found: audio`
- Remote config change:
  - backup created: `/root/.openclaw/openclaw.json.bak_20260328_101740`
  - removed `plugins.entries.audio`
  - added `tools.media.audio.enabled = true`
  - added `tools.media.audio.maxBytes = 20971520`
  - added direct-only audio scope
- Validation and restart:
  - `openclaw config validate` passes
  - background restart completed successfully
  - post-restart `openclaw status` remained healthy and no longer showed the stale audio warning
- Telegram bot menu updated through Bot API from the VPS.
- Final verified command set:
  - `new`
  - `status`
  - `reset`
  - `help`
  - `stop`

### 4. CURRENT STATE

- Gateway is healthy on `127.0.0.1:18789`.
- Telegram channel state is `ON / OK`.
- Security audit remains at `0 critical / 1 warn / 1 info`.
- The bot menu is now compact and Russian instead of the long default English list.
- The stale `plugins.entries.audio` warning is gone.
- Voice runtime prerequisites are present on the host:
  - Python `torch`
  - Python `whisper`
  - CLI `whisper`

### 5. NEXT STEP

- Ask the owner to send one real Telegram voice message to validate the full end-to-end voice-note ingestion path after the config migration.
- If that test passes, the current OpenClaw setup is stable enough to leave as-is.

### 6. RISKS / CAUTION

- Do not add unsupported slash commands to Telegram just because they look desirable; verify against `getMyCommands` first.
- Do not re-add `/restart` to the user-facing menu while `commands.restart = false` in the hardened configuration.
- Do not revert to the old `plugins.entries.audio` layout; current OpenClaw docs use `tools.media.audio`.
- If a reverse proxy or public UI is added later, configure `gateway.trustedProxies` and re-run the security audit.

### 7. DO NOT TOUCH

- Do not broaden the Telegram-exposed capability surface without a new security pass.
- Do not remove the new config backup created during this session.
- Do not restart `NemoClaw` work on this VPS until the capacity question is revisited.

### 8. CODE ARTIFACTS

- `research_notes.md`
- `implementation_plan.md`
- `task.md`
- `progress.md`
- `agent_audit.log`
- `.agents/handovers/handover_2026-03-28_openclaw-bot-menu-and-audio.md`

### 9. PROTOCOL VERSION

- AGENTS.md version: `v3.0.0`
- LLM used: `GPT-5 Codex`
