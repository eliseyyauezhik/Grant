param (
    [Parameter(Mandatory=$true)]
    [string[]]$Files,
    
    [Parameter(Mandatory=$false)]
    [string]$Message = "Checkpoint created"
)

# Base directories
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
# Calculate the project root (assuming .agents/skills/version-control/scripts/checkpoint.ps1)
$ProjectRoot = Resolve-Path (Join-Path $ScriptDir "..\..\..\..\") | Select-Object -ExpandProperty Path
$CheckpointsDir = Join-Path $ProjectRoot ".agents\checkpoints"

# Create checkpoints directory if it doesn't exist
if (-not (Test-Path $CheckpointsDir)) {
    New-Item -ItemType Directory -Force -Path $CheckpointsDir | Out-Null
}

# Generate checkpoint ID based on timestamp
$Timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$CheckpointId = "checkpoint_$Timestamp"
$CurrentCheckpointDir = Join-Path $CheckpointsDir $CheckpointId

# Create the specific checkpoint directory
New-Item -ItemType Directory -Force -Path $CurrentCheckpointDir | Out-Null

$ManifestPath = Join-Path $CurrentCheckpointDir "manifest.json"
$ManifestData = @{
    "id" = $CheckpointId
    "timestamp" = (Get-Date).ToString("o")
    "message" = $Message
    "files" = @()
}

$SuccessCount = 0
$FailedCount = 0

foreach ($File in $Files) {
    # Resolve absolute path for the file (could be relative to CWD or project root)
    if (Test-Path $File) {
        $SourceFile = Resolve-Path $File | Select-Object -ExpandProperty Path
    } else {
        $SourceFile = Join-Path $ProjectRoot $File
        if (-not (Test-Path $SourceFile)) {
            Write-Host "WARNING: File not found: $File" -ForegroundColor Yellow
            $FailedCount++
            continue
        }
    }

    # Calculate relative path from project root to recreate structure inside checkpoint (optional, but good for flat manifest)
    $RelativePath = $SourceFile.Replace($ProjectRoot, "").TrimStart("\")
    
    # Store flat in checkpoint dir but with unique hash or just flat name if no collision
    # For simplicity, we just use a hashed name or just the file name + index
    $SafeName = "{0}_{1}" -f $SuccessCount, (Split-Path $SourceFile -Leaf)
    $DestFile = Join-Path $CurrentCheckpointDir $SafeName
    
    try {
        Copy-Item -Path $SourceFile -Destination $DestFile -Force
        
        $FileInfo = @{
            "original_path" = $SourceFile
            "relative_path" = $RelativePath
            "checkpoint_name" = $SafeName
        }
        $ManifestData.files += $FileInfo
        $SuccessCount++
        Write-Host "Saved: $RelativePath" -ForegroundColor Green
    } catch {
        Write-Host "ERROR saving $File : $_" -ForegroundColor Red
        $FailedCount++
    }
}

# Save manifest
$ManifestData | ConvertTo-Json -Depth 5 | Out-File -FilePath $ManifestPath -Encoding UTF8

Write-Host "`n--- CHECKPOINT SUMMARY ---" -ForegroundColor Cyan
Write-Host "ID : $CheckpointId" -ForegroundColor Cyan
Write-Host "Message    : $Message"
Write-Host "Saved files: $SuccessCount"
Write-Host "Failed     : $FailedCount"
if ($SuccessCount -eq 0) {
    Write-Host "NO FILES SAVED. CHECKPOINT MIGHT BE USELESS." -ForegroundColor Yellow
} else {
    Write-Host "Use this ID to rollback if needed:`n"
    Write-Host "powershell -ExecutionPolicy Bypass -File `"$ScriptDir\rollback.ps1`" -CheckpointId `"$CheckpointId`"" -ForegroundColor Yellow
}
