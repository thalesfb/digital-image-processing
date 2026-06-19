# Install git hooks (Windows) - requires Git Bash
# Usage: pwsh scripts/git-hooks/install.ps1 [-RepoRoot "C:\dev\digital-image-processing"]

param(
    [string]$RepoRoot = ""
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

if (-not $RepoRoot) {
    $RepoRoot = git -C $ScriptDir rev-parse --show-toplevel 2>$null
    if (-not $RepoRoot) {
        $RepoRoot = Resolve-Path (Join-Path $ScriptDir "..\..")
    }
}

$bashExe = $null
$candidate = "C:\Program Files\Git\bin\bash.exe"
if (Test-Path $candidate) { $bashExe = $candidate }
if (-not $bashExe) {
    $bashCmd = Get-Command bash -ErrorAction SilentlyContinue
    if ($bashCmd) { $bashExe = $bashCmd.Source }
}
if (-not $bashExe) {
    Write-Error "Git Bash (bash.exe) required - install Git for Windows"
}

$repoUnix = ($RepoRoot -replace '\\', '/')
& $bashExe (Join-Path $ScriptDir "install.sh") $repoUnix
Write-Host "[OK] hooks installed via install.sh"
