# HANDOVER: NemoClaw OOM blocker on 4vps - 2026-03-28

## 1. SESSION TASK

Continue full `NemoClaw` onboarding on the 4vps Ubuntu host after user approval to interrupt the working `OpenClaw` service if needed.

## 2. DECISIONS MADE

1. No third onboarding retry was attempted after the second sandbox failure.
2. The second failure was treated as a blocker to diagnose, not as a prompt for random recovery attempts.
3. The working `OpenClaw` gateway was restored immediately after the failed retry.

## 3. IMPLEMENTED AND VERIFIED

- Verified by SSH that `OpenClaw` was already stopped and `18789` was free before retrying `NemoClaw`.
- Created fresh backup archives:
  - `/root/nemoclaw-backups/openclaw_pre_resume_20260328_003059.tgz`
  - `/root/nemoclaw-backups/nemoclaw_pre_resume_20260328_003059.tgz`
- Ran `nemoclaw onboard --resume --non-interactive` with Anthropic credentials.
- Verified the retry rebuilt sandbox image `openshell/sandbox-from:1774654357`.
- Captured the actual failure point from logs: `openshell sandbox create` was terminated with `Killed`.
- Confirmed via `dmesg -T` and `journalctl -k` that the host hit global OOM during sandbox creation.
- Restored `OpenClaw` with `openclaw gateway start`.
- Verified rollback state:
  - `openclaw-gateway.service` running
  - `127.0.0.1:18789` listening
  - `OpenClaw status` shows gateway reachable
  - Telegram channel `ON / OK`

## 4. CURRENT STATE

`NemoClaw` onboarding is still incomplete. `gateway` and `inference` were completed, but the `sandbox` step failed again. No sandboxes are registered in `nemoclaw list`. `OpenClaw` is back online and usable.

## 5. ROOT CAUSE

The blocker is host memory, not port conflict:

- VPS memory: `3.8 GiB`
- Swap: `0 B`
- Kernel logs confirm OOM kill for the relevant `openshell` process during sandbox creation/export.

## 6. NEXT STEP

Before retrying `NemoClaw`, change VPS memory conditions:

1. Add swap on the current server, or
2. Upgrade to a higher-RAM VPS plan.

After that, rerun:

```bash
ANTHROPIC_API_KEY=... nemoclaw onboard --resume --non-interactive
```

## 7. ROLLBACK / SAFE COMMANDS

If `OpenClaw` needs to be restored again:

```bash
openclaw gateway start
openclaw status
ss -ltnp | grep ':18789'
```

## 8. KEY FILES / ARTIFACTS

- Local notes: `research_notes.md`, `implementation_plan.md`, `task.md`, `progress.md`
- Remote backup folder: `/root/nemoclaw-backups`
- Remote session file: `/root/.nemoclaw/onboard-session.json`
- Remote retry log: latest `/root/nemoclaw-resume-*.log`
