param (
    [Parameter(Mandatory = $true)]
    [string]$CheckpointId
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Resolve-Path (Join-Path $ScriptDir "..\..\..\..\") | Select-Object -ExpandProperty Path
$CheckpointsDir = Join-Path $ProjectRoot ".agents\checkpoints"

$TargetCheckpointDir = Join-Path $CheckpointsDir $CheckpointId

if (-not (Test-Path $TargetCheckpointDir)) {
    Write-Host "ERROR: Checkpoint folder not found -> $TargetCheckpointDir" -ForegroundColor Red
    exit 1
}

$ManifestPath = Join-Path $TargetCheckpointDir "manifest.json"
if (-not (Test-Path $ManifestPath)) {
    Write-Host "ERROR: Manifest not found in checkpoint folder -> $ManifestPath" -ForegroundColor Red
    exit 1
}

$ManifestData = Get-Content -Path $ManifestPath -Raw | ConvertFrom-Json

Write-Host "Rolling back to Checkpoint: $($ManifestData.id)" -ForegroundColor Cyan
Write-Host "Created at: $($ManifestData.timestamp)"
Write-Host "Message   : $($ManifestData.message)"
Write-Host "-------------------------------"

$SuccessCount = 0
$FailedCount = 0

foreach ($FileObj in $ManifestData.files) {
    # File locations
    $BackupFile = Join-Path $TargetCheckpointDir $FileObj.checkpoint_name
    $DestFile = $FileObj.original_path

    if (-not (Test-Path $BackupFile)) {
        Write-Host "ERROR: Backup file is missing inside checkpoint folder -> $BackupFile" -ForegroundColor Red
        $FailedCount++
        continue
    }

    try {
        # Check if destination directory exists, if not create it
        $DestDir = Split-Path -Parent $DestFile
        if (-not (Test-Path $DestDir)) {
            New-Item -ItemType Directory -Force -Path $DestDir | Out-Null
        }

        # Copy file back to its original location
        Copy-Item -Path $BackupFile -Destination $DestFile -Force
        $SuccessCount++
        Write-Host "Restored: $($FileObj.relative_path)" -ForegroundColor Green
    }
    catch {
        Write-Host "ERROR restoring $($FileObj.relative_path) : $_" -ForegroundColor Red
        $FailedCount++
    }
}

Write-Host "`n--- ROLLBACK SUMMARY ---" -ForegroundColor Cyan
Write-Host "Restored files: $SuccessCount"
Write-Host "Failed        : $FailedCount"

if ($SuccessCount -gt 0) {
    Write-Host "Rollback completed successfully." -ForegroundColor Green
}
else {
    Write-Host "Rollback likely failed." -ForegroundColor Red
}
