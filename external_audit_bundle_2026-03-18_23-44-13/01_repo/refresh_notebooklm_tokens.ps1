param(
    [int]$DebugPort = 9222,
    [string]$TargetUrl = 'https://notebooklm.google.com/'
)

$ErrorActionPreference = 'Stop'

$pythonPath = 'C:\Users\Admin\.gemini\antigravity\venv\Scripts\python.exe'
$scriptPath = Join-Path $PSScriptRoot 'notebooklm_auto_refresh.py'

if (-not (Test-Path $pythonPath)) {
    throw "Python was not found: $pythonPath"
}

if (-not (Test-Path $scriptPath)) {
    throw "Script was not found: $scriptPath"
}

& $pythonPath $scriptPath --debug-port $DebugPort --target-url $TargetUrl
exit $LASTEXITCODE
