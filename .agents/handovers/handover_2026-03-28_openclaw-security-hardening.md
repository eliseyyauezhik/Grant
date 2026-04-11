## HANDOVER: OpenClaw 4vps security hardening — 2026-03-28

### 1. SESSION TASK

Keep the project on `OpenClaw` only, harden the live VPS deployment for single-owner Telegram use, and produce a detailed project dossier for external LLM review.

### 2. DECISIONS MADE

- `NemoClaw` is deferred. The current VPS plan is still too disk-constrained for reliable onboarding.
- The active target is a secure, stable `OpenClaw` baseline, not a feature-rich automation profile.
- Telegram groups were explicitly disabled because they were not actually usable in the current allowlist-based config and only widened the trust-model warning surface.
- Runtime/filesystem/UI/node automation surfaces were intentionally denied.

### 3. IMPLEMENTED AND VERIFIED

- Live VPS hardening:
  - enabled `agents.defaults.sandbox.mode = all`
  - set `sandbox.scope = agent`
  - set `sandbox.workspaceAccess = none`
  - switched `tools.profile` from `coding` to `messaging`
  - allowed only `image` beyond messaging defaults
  - denied `group:automation`, `group:runtime`, `group:fs`, `group:ui`, `group:nodes`, `sessions_spawn`, `sessions_send`
  - disabled `tools.elevated`
  - set `tools.exec.security = deny`
  - set `tools.fs.workspaceOnly = true`
  - set `commands.restart = false`
  - disabled Telegram groups
- Removed obsolete `gateway.nodes.denyCommands`.
- Tightened remote permissions:
  - `/root/.openclaw` -> `700`
  - `/root/.openclaw/openclaw.json` -> `600`
  - `/root/.openclaw/agents/main/agent/auth-profiles.json` -> `600`
- Added low-risk token tuning:
  - `cacheRetention = long`
  - `contextPruning = cache-ttl / 1h`
- Disabled `memorySearch` after confirming no embedding provider was configured and the feature only produced operational noise.
- Cleaned two accidental quoted model keys from `/root/.openclaw/openclaw.json`.

Verified:
- `openclaw config validate` passes
- `openclaw status` shows gateway reachable on `127.0.0.1:18789`
- Telegram is `ON / OK`
- `openclaw security audit --json` is down to `0 critical / 1 warn / 1 info`
- remaining warning is only `gateway.trusted_proxies_missing`

### 4. CURRENT STATE

Current live operating model:
- local-only gateway on loopback
- Telegram DM-oriented assistant
- no Telegram groups
- no host-level elevated execution
- no runtime/filesystem/UI/node automation tool surface exposed to chat-driven turns

Useful remote backups created during this stage:
- `/root/.openclaw/openclaw.json.bak_20260328_020925`
- `/root/.openclaw/openclaw.json.bak_20260328_021123`
- `/root/.openclaw/openclaw.json.bak_20260328_021510`

The final sanitized project summary is in `openclaw_project_dossier_2026-03-28.md`.

### 5. NEXT STEP

If continuing this project later, the first decision should be:
- leave `OpenClaw` as-is and only document/operate it
- or selectively re-enable additional capability in a staged way, starting with a conscious decision on memory search and sandbox base image preparation

### 6. RISKS / CAUTION

- Do not expose port `18789` directly to the internet.
- If a reverse proxy or Tailscale Serve is added later, configure `gateway.trustedProxies` and re-run `openclaw security audit --deep`.
- `openclaw doctor` still notes the sandbox base image is missing. This is non-blocking now, but it matters before any future re-enable of runtime/filesystem tools.
- Memory search is explicitly disabled now. Re-enable it only together with a deliberate embedding-provider setup.
- Do not re-enable `tools.elevated` casually.

### 7. DO NOT TOUCH

- Do not restart `NemoClaw` work on this VPS unless disk capacity is increased first.
- Do not remove the current `OpenClaw` config backups.
- Do not broaden the tool surface from Telegram without a new explicit hardening pass.

### 8. CODE ARTIFACTS

- Local artifacts:
  - `research_notes.md`
  - `implementation_plan.md`
  - `task.md`
  - `progress.md`
  - `agent_audit.log`
  - `openclaw_project_dossier_2026-03-28.md`
- Remote key files:
  - `/root/.openclaw/openclaw.json`
  - `/root/.openclaw/agents/main/agent/auth-profiles.json`

### 9. PROTOCOL VERSION

- AGENTS.md version: `v3.0.0`
- LLM used: `GPT-5 Codex`
