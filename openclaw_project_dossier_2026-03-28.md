# OpenClaw Project Dossier — 2026-03-28

Status
- `OpenClaw` is working on the current VPS and has been hardened for single-owner Telegram use.
- `NemoClaw` is intentionally deferred; it is not part of the active deployment now.

## 1. Project Goal

The project goal is to keep a stable self-hosted `OpenClaw` assistant on the current `4vps` Linux VPS, reachable through Telegram, while minimizing unnecessary attack surface. The user explicitly decided to pause `NemoClaw` for now because the current VPS plan is too tight for it.

This document is written for another LLM or engineer who needs a verified snapshot of the current system, not a marketing summary.

## 2. Environment

Verified environment facts:
- Host OS: `Ubuntu 22.04.5 LTS`
- Public host: `4vps` Linux VPS
- OpenClaw version: `2026.3.24 (cff6dc9)`
- Gateway mode: local
- Gateway bind: loopback
- Gateway port: `18789`
- Current access channel: Telegram
- Current deployment choice: `OpenClaw` only

Important boundary:
- The gateway is intentionally local-only on `127.0.0.1:18789`.
- There is no current requirement to expose the Control UI directly to the public internet.

## 3. What Happened Before This State

Earlier in the same operating thread:
- `OpenClaw` was installed and made stable on the VPS.
- `NemoClaw` onboarding was attempted multiple times.
- Initial `NemoClaw` blockers were:
  - port `18789` conflict
  - OOM during `openshell sandbox create`
  - then disk exhaustion during final sandbox materialization
- The VPS was recovered after the final `NemoClaw` failure:
  - failed `openshell-cluster-nemoclaw` runtime artifacts were removed
  - free disk returned to about `3.9G`
  - `OpenClaw` was restored and verified working again

The current decision is to stop pushing `NemoClaw` on this tariff and instead solidify `OpenClaw`.

## 4. Verified Current Runtime State

Verified after hardening:
- `openclaw status` shows the gateway reachable on `127.0.0.1:18789`
- Telegram channel state is `ON / OK`
- `openclaw security audit --json` shows:
  - `0 critical`
  - `1 warn`
  - `1 info`
- Tightened host-side permissions:
  - `/root/.openclaw` -> `700`
  - `/root/.openclaw/openclaw.json` -> `600`
  - `/root/.openclaw/agents/main/agent/auth-profiles.json` -> `600`

Residual audit warning:
- `gateway.trusted_proxies_missing`

Meaning of the residual warning:
- It is relevant only if someone later places a reverse proxy or another HTTP forwarding layer in front of the loopback gateway.
- In the current loopback-only state it is not an active exploit path by itself.

## 5. Final Sanitized Config Summary

Secrets are intentionally omitted below.

```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "anthropic/claude-sonnet-4-6"
      },
      "models": {
        "anthropic/claude-sonnet-4-6": {
          "params": {
            "cacheRetention": "long"
          }
        }
      },
      "contextPruning": {
        "mode": "cache-ttl",
        "ttl": "1h"
      },
      "sandbox": {
        "mode": "all",
        "workspaceAccess": "none",
        "scope": "agent"
      },
      "workspace": "/root/.openclaw/workspace"
    }
  },
  "tools": {
    "profile": "messaging",
    "allow": ["image"],
    "deny": [
      "group:automation",
      "group:runtime",
      "group:fs",
      "group:ui",
      "group:nodes",
      "sessions_spawn",
      "sessions_send"
    ],
    "fs": {
      "workspaceOnly": true
    },
    "exec": {
      "security": "deny",
      "ask": "always"
    },
    "elevated": {
      "enabled": false
    }
  },
  "commands": {
    "restart": false
  },
  "session": {
    "dmScope": "per-channel-peer"
  },
  "channels": {
    "telegram": {
      "enabled": true,
      "dmPolicy": "pairing",
      "groupPolicy": "disabled",
      "streaming": "partial"
    }
  },
  "gateway": {
    "mode": "local",
    "bind": "loopback",
    "port": 18789,
    "auth": {
      "mode": "token"
    },
    "tailscale": {
      "mode": "off"
    }
  }
}
```

Important nuance:
- `tools.web.search.enabled = true` still exists in the raw config, but the active tool profile and deny set keep the web tool surface unavailable in practice.
- This was left intentionally as a future reversible option, not as an active capability.

## 6. What Changed During Hardening

Initial risky settings:
- `tools.profile = coding`
- sandbox off
- host-level elevated execution enabled
- filesystem unrestricted to workspace
- Telegram groups logically configured
- ineffective `gateway.nodes.denyCommands`

Applied hardening:
- enabled sandboxing for all agent turns
- removed host escape hatch (`tools.elevated.enabled = false`)
- switched to `messaging` tool profile
- allowed only `image` beyond messaging defaults
- denied runtime, filesystem, UI, nodes, automation, session-spawn, and session-send tools
- forced filesystem operations to stay workspace-only even if re-enabled later
- disabled Telegram groups explicitly
- removed dead node deny rules
- disabled manual restart command path
- tightened file permissions on OpenClaw state
- added low-risk token-efficiency tuning:
  - `cacheRetention = long`
  - `contextPruning = cache-ttl / 1h`

## 7. Why This Shape Was Chosen

This is a deliberate compromise:
- safer than the original `coding` profile
- still useful for Telegram chat and image understanding
- does not rely on public exposure
- does not re-open the host shell/filesystem surface to Telegram messages

The configuration now matches the documented OpenClaw single-owner trust model much better:
- one trusted operator boundary
- no groups
- no host exec escalation
- no filesystem/runtime tools available to chat-driven turns

## 8. Remaining Non-Blocking Issues

### 8.1 Reverse proxy warning

`openclaw security audit` still warns about `trustedProxies`.

Interpretation:
- ignore for now while the gateway stays loopback-only
- configure only if a reverse proxy or Tailscale Serve is added later

### 8.2 Sandbox base image not prepared

`openclaw doctor` reports:
- `Sandbox base image missing: openclaw-sandbox:bookworm-slim`

Interpretation:
- non-blocking today because runtime/fs/ui/node tools are denied
- required before any future re-enable of shell/file tooling
- should be treated carefully because this VPS has limited disk headroom

### 8.3 Memory search disabled on purpose

During the hardening pass, `memory search` was explicitly disabled.

Interpretation:
- before disabling it, live checks showed:
  - `Provider: none`
  - `Embeddings: unavailable`
- leaving it enabled would only create operational noise and a false expectation of semantic recall
- if semantic recall is needed later, re-enable it only together with an explicit embedding-provider decision

## 9. Operating Guide

### 9.1 Daily health checks

Use these commands on the VPS:

```bash
openclaw status
openclaw security audit --json
openclaw doctor
ss -ltnp | grep 18789
```

Expected healthy indicators:
- gateway reachable on `127.0.0.1:18789`
- Telegram `ON / OK`
- security audit remains at `0 critical`

### 9.2 Config and state locations

Important remote paths:
- config: `/root/.openclaw/openclaw.json`
- workspace: `/root/.openclaw/workspace`
- agent auth store: `/root/.openclaw/agents/main/agent/auth-profiles.json`
- sessions: `/root/.openclaw/agents/main/sessions/`

### 9.3 Safe maintenance commands

```bash
openclaw config validate
openclaw logs --follow
openclaw gateway probe
openclaw gateway start
openclaw gateway stop
```

### 9.4 What not to do casually

Do not do these without an intentional change window:
- do not expose `18789` directly to the internet
- do not switch Telegram `groupPolicy` back to `open`
- do not re-enable `group:runtime` or `group:fs` from chat-facing agents without preparing sandbox runtime properly
- do not enable `tools.elevated`
- do not place secrets into chat, notes, or external LLM prompts

## 10. If More Capability Is Needed Later

### Case A: external Control UI access

Recommended path:
1. keep gateway bind loopback
2. add reverse proxy or Tailscale Serve
3. explicitly configure `gateway.trustedProxies`
4. re-run `openclaw security audit --deep`

### Case B: shell or file operations

Recommended path:
1. first build the sandbox base image
2. verify disk headroom on the VPS
3. re-enable only the minimum required tools
4. prefer a separate trusted agent or separate host if capabilities broaden substantially

### Case C: smarter memory

Choose one:
- keep the current disabled state
- or re-enable memory search only together with an embedding provider and verification via `openclaw memory status --deep`

## 11. Questions For Another LLM

Useful questions for a second model review:
- Is this hardened OpenClaw baseline internally coherent for a single-owner Telegram assistant?
- Would you disable memory search entirely on this VPS, or keep it pending future embeddings?
- If shell/filesystem tools must return later, what is the cleanest staged re-enable plan on a low-disk VPS?
- Is there a better minimal external-access strategy than reverse proxy plus `trustedProxies` for this setup?
- Which exact OpenClaw settings would you add or remove next without making the system materially riskier?

## 12. Local Project Artifacts

Local files updated during this stage:
- `research_notes.md`
- `implementation_plan.md`
- `task.md`
- `progress.md`
- `agent_audit.log`
- `.agents/handovers/handover_2026-03-28_openclaw-security-hardening.md`
- `openclaw_project_dossier_2026-03-28.md`

This file is the recommended single document to hand to another LLM first.
