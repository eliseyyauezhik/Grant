[CmdletBinding()]
param(
    [ValidateSet("show", "governance", "youtube", "notebooklm", "workspace", "site", "all")]
    [string]$Cohort = "show",
    [switch]$Apply,
    [switch]$ResetIndexFirst,
    [switch]$ExcludeGenerated,
    [switch]$ShowStatus
)

$ErrorActionPreference = "Stop"

$Cohorts = [ordered]@{
    governance = @(
        "AGENTS.md",
        ".agents/skills/safety-guardrails/SKILL.md",
        "research_notes.md",
        "implementation_plan.md",
        "task.md",
        "progress.md",
        "agent_audit.log"
    )
    youtube = @(
        ".agents/skills/youtube-monitoring/SKILL.md",
        ".agents/skills/youtube-monitoring/references/reference.md",
        ".agents/skills/youtube-monitoring/scripts/mcp_server.py",
        ".agents/skills/youtube-monitoring/scripts/requirements.txt",
        ".agents/skills/youtube-monitoring/scripts/skill.py",
        ".agents/skills/youtube-monitoring/tests/test_core.py"
    )
    notebooklm = @(
        "launch_notebooklm_debug_chrome.ps1",
        "notebooklm_auto_refresh.py",
        "refresh_notebooklm_tokens.ps1",
        "run_nlm_proxy.ps1"
    )
    workspace = @(
        "workspace/"
    )
    site = @(
        "index_v3.html",
        "PROJECT_LINKS.md",
        "_bases_syntax.html",
        "_obsidian_cli_help.html",
        "transcript.txt",
        "transcript_utf8.txt",
        "1_infographics_optimized.jpg",
        "1_infographics_optimized.webp",
        "gymnasium_photo_opt.jpg",
        "gymnasium_photo_opt.webp"
    )
    generated = @(
        ".agents/checkpoints/",
        "__pycache__/",
        ".agents/skills/youtube-monitoring/scripts/__pycache__/",
        ".agents/skills/youtube-monitoring/scripts/logs/",
        ".agents/skills/youtube-monitoring/tests/__pycache__/",
        ".agents/skills/youtube-monitoring/tests/tmp_kb/"
    )
}

function Invoke-Git {
    param(
        [string[]]$GitArgs
    )
    if ($Apply) {
        & git @GitArgs
    } else {
        "git $([string]::Join(' ', $GitArgs))"
    }
}

function Stage-Cohort {
    param(
        [string]$Name
    )
    $paths = $Cohorts[$Name]
    if (-not $paths) {
        throw "Unknown cohort: $Name"
    }
    $gitArgs = @("add", "--") + $paths
    Invoke-Git -GitArgs $gitArgs
}

function Unstage-Generated {
    $paths = $Cohorts.generated
    $gitArgs = @("restore", "--staged", "--") + $paths
    Invoke-Git -GitArgs $gitArgs
}

if ($Cohort -eq "show") {
    "Available cohorts:"
    foreach ($name in $Cohorts.Keys) {
        if ($name -eq "generated") {
            continue
        }
        "- $name"
    }
    "Use -ResetIndexFirst and -ExcludeGenerated to build a clean index."
    exit 0
}

if ($ResetIndexFirst) {
    Invoke-Git -GitArgs @("restore", "--staged", ".")
}

if ($Cohort -eq "all") {
    Stage-Cohort -Name "governance"
    Stage-Cohort -Name "youtube"
    Stage-Cohort -Name "notebooklm"
    Stage-Cohort -Name "workspace"
    Stage-Cohort -Name "site"
} else {
    Stage-Cohort -Name $Cohort
}

if ($ExcludeGenerated) {
    Unstage-Generated
}

if ($ShowStatus) {
    Invoke-Git -GitArgs @("status", "--short")
}
