# Staging Strategy (No Commit)

This strategy prepares deterministic staging by thematic cohorts without creating a commit.

## Current Index State

- The index is currently over-staged (most files are already staged).
- Start from a clean index baseline before staging any cohort.

## Baseline

```powershell
git restore --staged .
```

## Stage One Cohort

```powershell
powershell -File .\scripts\git_cohort_stage.ps1 -Cohort governance -Apply -ShowStatus
```

Available cohort values:

- `governance`
- `youtube`
- `notebooklm`
- `workspace`
- `site`
- `all`

## Dry Run (Preview Commands)

```powershell
powershell -File .\scripts\git_cohort_stage.ps1 -Cohort youtube -ResetIndexFirst -ExcludeGenerated -ShowStatus
```

No index changes are made unless `-Apply` is provided.

## Full Stage Plan (Still No Commit)

```powershell
git restore --staged .
powershell -File .\scripts\git_cohort_stage.ps1 -Cohort governance -Apply -ExcludeGenerated -ShowStatus
powershell -File .\scripts\git_cohort_stage.ps1 -Cohort youtube -Apply -ExcludeGenerated -ShowStatus
powershell -File .\scripts\git_cohort_stage.ps1 -Cohort notebooklm -Apply -ExcludeGenerated -ShowStatus
powershell -File .\scripts\git_cohort_stage.ps1 -Cohort workspace -Apply -ExcludeGenerated -ShowStatus
powershell -File .\scripts\git_cohort_stage.ps1 -Cohort site -Apply -ExcludeGenerated -ShowStatus
```

## Exclude Generated Artifacts

```powershell
git restore --staged -- .agents/checkpoints/ __pycache__/ .agents/skills/youtube-monitoring/scripts/__pycache__/ .agents/skills/youtube-monitoring/scripts/logs/ .agents/skills/youtube-monitoring/tests/__pycache__/ .agents/skills/youtube-monitoring/tests/tmp_kb/
```

## Validation Before Any Commit

```powershell
git status --short
git diff --cached --name-only
```

## Cohort Checkpoint Mapping

- `governance` -> `checkpoint_20260318_023712`
- `youtube` -> `checkpoint_20260318_023808`
- `notebooklm` -> `checkpoint_20260318_023809`
- `workspace` -> `checkpoint_20260318_023811`
- `site` -> `checkpoint_20260318_023813`
- `checkpoint_20260318_023731` is mixed and should not be used for rollback.
