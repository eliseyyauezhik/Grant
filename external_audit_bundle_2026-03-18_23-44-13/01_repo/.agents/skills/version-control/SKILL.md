---
name: version-control
description: Create local checkpoints and restore them when risky edits need a safe rollback path. Use when changing existing files in the workspace and a reversible checkpoint is needed first. Do NOT use for git workflows, commits, or reverting unrelated user changes.
---

# Version Control

## Overview

Use local checkpoints in `.agents/checkpoints/` before risky edits. Apply `core-agent-rules` first for writable roots, dirty-state awareness, and approval boundaries before checkpointing or rolling back files.

## When to Use

- Before broad replacements, regex edits, or scripted rewrites.
- Before editing agent-system files such as `AGENTS.md` or `.agents/skills/**`.
- When the user asks to preserve a known-good variant before experimentation.
- When a failed edit should be reverted to a checkpointed state.

## Workflow

1. Choose only files inside the current workspace or other writable roots.
2. Inspect whether the target files contain unrelated user changes before saving or restoring.
3. Create a checkpoint with `scripts/checkpoint.ps1`.
4. Record the returned checkpoint ID in the task notes or final report.
5. If rollback is needed, restore only the files covered by that checkpoint.

### Create Checkpoint

Run:

```powershell
powershell -ExecutionPolicy Bypass -File ".agents\skills\version-control\scripts\checkpoint.ps1" -Files "index_v3.html", "style.css"
```

The script returns a checkpoint ID such as `checkpoint_20260318_004504`.

### Roll Back

Run:

```powershell
powershell -ExecutionPolicy Bypass -File ".agents\skills\version-control\scripts\rollback.ps1" -CheckpointId "20260307_123456"
```

Rollback restores the files captured by that checkpoint. Do not use rollback to overwrite unrelated user edits unless the user explicitly approves it.

## Stored Data

- `.agents/checkpoints/<ID>/` stores the checkpointed file copies.
- `.agents/checkpoints/<ID>/manifest.json` maps each saved file back to its original location.

## Common Mistakes

- Checkpointing large binary directories such as `node_modules`. Fix: checkpoint only the specific source files being changed.
- Forgetting the checkpoint ID. Fix: write it into the task notes or final report immediately.
- Using rollback on files with mixed user and agent edits. Fix: inspect dirty state first and ask before overwriting unrelated work.
- Referring to a legacy command runner that is not available here. Fix: use the current shell or PowerShell execution tool.
