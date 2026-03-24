param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$NlmArgs
)

$ErrorActionPreference = 'Stop'

$configPath = 'C:\Users\Admin\.gemini\antigravity\mcp_config.json'
$nlmPath = 'C:\Users\Admin\.gemini\antigravity\venv\Scripts\nlm.exe'

if (-not (Test-Path $configPath)) {
    throw "Config file not found: $configPath"
}

if (-not (Test-Path $nlmPath)) {
    throw "nlm.exe was not found: $nlmPath"
}

$config = Get-Content -Raw -Encoding UTF8 $configPath | ConvertFrom-Json
$server = $config.mcpServers.'notebooklm-mcp'
if (-not $server) {
    throw "notebooklm-mcp config entry was not found"
}

$env:HTTP_PROXY = $server.env.HTTP_PROXY
$env:HTTPS_PROXY = $server.env.HTTPS_PROXY
$env:PYTHONIOENCODING = 'utf-8'

if (-not $NlmArgs -or $NlmArgs.Count -eq 0) {
    $NlmArgs = @('--help')
}

& $nlmPath @NlmArgs
exit $LASTEXITCODE
