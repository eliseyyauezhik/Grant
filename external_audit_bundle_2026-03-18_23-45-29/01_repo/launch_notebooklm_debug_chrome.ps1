param(
    [int]$RemoteDebugPort = 9222,
    [string]$NotebookUrl = 'https://notebooklm.google.com/',
    [string]$ChromePath = "$env:ProgramFiles\Google\Chrome\Application\chrome.exe",
    [string]$ProfileDir = "$env:LOCALAPPDATA\Google\Chrome\User Data NotebookLM",
    [switch]$PrintOnly
)

$ErrorActionPreference = 'Stop'

$configPath = 'C:\Users\Admin\.gemini\antigravity\mcp_config.json'
if (-not (Test-Path $configPath)) {
    throw "Config file not found: $configPath"
}

if (-not (Test-Path $ChromePath)) {
    throw "Chrome not found: $ChromePath"
}

$config = Get-Content -Raw -Encoding UTF8 $configPath | ConvertFrom-Json
$server = $config.mcpServers.'notebooklm-mcp'
if (-not $server) {
    throw "notebooklm-mcp config entry was not found"
}

$proxyUrl = $server.env.HTTPS_PROXY
if (-not $proxyUrl) {
    $proxyUrl = $server.env.HTTP_PROXY
}
if (-not $proxyUrl) {
    throw "Proxy settings were not found in notebooklm-mcp env"
}

$proxyUri = [Uri]$proxyUrl
$proxyServer = '{0}://{1}:{2}' -f $proxyUri.Scheme, $proxyUri.Host, $proxyUri.Port
$argumentList = @(
    "--proxy-server=$proxyServer",
    "--remote-debugging-port=$RemoteDebugPort",
    "--user-data-dir=$ProfileDir",
    $NotebookUrl
)

if ($PrintOnly) {
    [PSCustomObject]@{
        chrome_path       = $ChromePath
        proxy_server      = $proxyServer
        remote_debug_port = $RemoteDebugPort
        profile_dir       = $ProfileDir
        notebook_url      = $NotebookUrl
        arguments         = $argumentList -join ' '
    } | ConvertTo-Json -Depth 3
    exit 0
}

Start-Process -FilePath $ChromePath -ArgumentList $argumentList | Out-Null
Write-Output "Chrome started with remote debugging on port $RemoteDebugPort"
Write-Output "If Chrome asks for proxy credentials, enter them once in the browser dialog."
