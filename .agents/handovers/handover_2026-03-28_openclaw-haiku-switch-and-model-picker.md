## HANDOVER: OpenClaw Haiku switch and Telegram model picker — 2026-03-28

### 1. SESSION TASK

Lower OpenClaw operating cost on the VPS by switching the default Anthropic model from Sonnet to Haiku, while also exposing model switching directly inside the Telegram bot and notifying the owner in Telegram when the work is complete.

### 2. DECISIONS MADE

- Chose `Anthropic Haiku` instead of a Google model because Anthropic auth was already configured and verified live on the VPS.
- Kept `Anthropic Sonnet` as the only fallback so the cheaper default still has a stronger recovery path.
- Kept the change scoped to the current owner/Telegram workflow and did not introduce new providers, keys, or architectural changes.
- Added `/model` to the Telegram command menu instead of inventing a custom pseudo-menu, because OpenClaw already supports native in-chat model switching.

### 3. IMPLEMENTED AND VERIFIED

- Remote config updates applied to `/root/.openclaw/openclaw.json`:
  - primary model -> `anthropic/claude-haiku-4-5-20251001`
  - fallbacks -> `["anthropic/claude-sonnet-4-6"]`
  - allowlist -> `haiku` + `sonnet`
  - cache retention kept on both entries
- Fresh backups created:
  - `/root/.openclaw/openclaw.json.bak_20260328_163658`
  - `/root/.openclaw/openclaw.json.bak_20260328_163957`
  - `/root/.openclaw/agents/main/sessions/sessions.json.bak_20260328_163957`
- Owner Telegram session mappings removed from `/root/.openclaw/agents/main/sessions/sessions.json`.
- Gateway restart completed successfully through:
  - `openclaw gateway restart`
  - result: `openclaw-gateway.service`
- Telegram owner/private menus re-published via Bot API:
  - owner menu now includes `/model`
  - owner menu order:
    - `new`
    - `reset`
    - `model`
    - `status`
    - `restart`
    - `stop`
    - `help`
    - `commands`
- Final verification:
  - `openclaw config validate` -> valid
  - `openclaw models status --plain` -> `anthropic/claude-haiku-4-5-20251001`
  - `openclaw status --deep` -> gateway reachable, Telegram `ON / OK`
  - `sessions.json` contains only `agent:main:main`
- Completion message was sent to the owner Telegram chat successfully (`message id 137`).

### 4. CURRENT STATE

- New Telegram DMs should start on `Haiku`.
- The owner can switch models directly from Telegram with:
  - `/model`
  - `/model list`
  - `/model haiku`
  - `/model sonnet`
  - `/model status`
- The previous owner direct/slash sessions were deliberately cleared, so the model change takes effect on the next real chat start instead of waiting for old session state.

### 5. NEXT STEP

- Manually test in Telegram:
  - `/model`
  - `/model haiku`
  - `/model sonnet`
  - a fresh normal message after `/new`
- If needed later, add more models to the allowlist or switch to a Google provider only after adding and validating Google auth.

### 6. RISKS / CAUTION

- OpenClaw now reports an additional non-critical security warning because `Haiku` is a smaller tier model.
- This is an explicit owner-requested cost tradeoff; `Sonnet` remains available as fallback and manual switch target.
- The internal non-Telegram session `agent:main:main` still shows historical Sonnet state, but the owner Telegram session keys were removed and are the relevant path for real bot usage.

### 7. DO NOT TOUCH

- Do not remove `anthropic/claude-sonnet-4-6` from fallbacks unless a different safe fallback is added first.
- Do not remove `/model` from the owner Telegram menu unless a better in-bot model selector is already ready.
- Do not switch providers without explicitly validating credentials and the allowlist again.

### 8. CODE ARTIFACTS

- `research_notes.md`
- `implementation_plan.md`
- `task.md`
- `progress.md`
- `agent_audit.log`
- `workspace/projects/my-backlog.md`
- `.agents/handovers/handover_2026-03-28_openclaw-haiku-switch-and-model-picker.md`

### 9. PROTOCOL VERSION

- AGENTS.md version: `v3.0.0`
- LLM used: `GPT-5 Codex`
