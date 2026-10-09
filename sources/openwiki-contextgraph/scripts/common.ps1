# Shared helpers for the POC scripts. Dot-source: . "$PSScriptRoot\common.ps1"

$ErrorActionPreference = 'Stop'

$Script:ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$Script:OpenWikiVersion = '0.7.0'

function Write-Step([string]$Message) {
    Write-Host "==> $Message" -ForegroundColor Cyan
}

function Read-DotEnv([string]$Path) {
    # Returns a hashtable of KEY=VALUE pairs; ignores blank lines and # comments.
    $values = @{}
    if (-not (Test-Path $Path)) { return $values }
    foreach ($line in Get-Content $Path) {
        $trimmed = $line.Trim()
        if ($trimmed -eq '' -or $trimmed.StartsWith('#')) { continue }
        $idx = $trimmed.IndexOf('=')
        if ($idx -lt 1) { continue }
        $values[$trimmed.Substring(0, $idx).Trim()] = $trimmed.Substring($idx + 1).Trim()
    }
    return $values
}

function Write-Utf8NoBom([string]$Path, [string]$Content) {
    # PowerShell 5.1's -Encoding utf8 adds a BOM, which breaks JSON.parse and ignore patterns.
    [System.IO.File]::WriteAllText($Path, $Content, (New-Object System.Text.UTF8Encoding $false))
}

function Initialize-OpenWikiOnboarding([string]$ConfigDir) {
    # Code-mode onboarding record. Written directly so OpenWiki --init/--update never need the
    # interactive setup; the wiki goal itself is read from each repo's openwiki/INSTRUCTIONS.md.
    New-Item -ItemType Directory -Force -Path $ConfigDir | Out-Null
    $onboarding = Join-Path $ConfigDir 'onboarding.json'
    if (Test-Path $onboarding) { return }
    Write-Step 'Writing OpenWiki code-mode onboarding.json'
    $record = [ordered]@{
        version         = 1
        completedAt     = (Get-Date).ToUniversalTime().ToString('o')
        modeId          = 'code'
        modeName        = 'Code'
        sourceInstances = @()
        sources         = @{}
    }
    Write-Utf8NoBom $onboarding ($record | ConvertTo-Json -Depth 4)
}

function Initialize-CorpusRepo([string]$Corpus, [string]$Message) {
    # OpenWiki only accepts a wiki root that is its own git repository (it resolves `git rev-parse
    # --show-toplevel`), so a corpus inside the project repo needs its own .git.
    Push-Location $Corpus
    try {
        & git init --quiet
        & git config core.autocrlf false
        if (-not (& git config user.email)) {
            & git config user.email 'poc@openwiki.local'
            & git config user.name 'OpenWiki POC'
        }
        & git add -A
        & git commit --quiet -m $Message
        if ($LASTEXITCODE -ne 0) { throw "git commit failed in $Corpus" }
    } finally { Pop-Location }
}

function Restore-SemanticCorpus([string]$Corpus) {
    # Restores the prebuilt semantic wiki shipped in prebuilt/semantic-corpus (no 45 min OpenWiki build).
    $prebuilt = Join-Path $Script:ProjectRoot 'prebuilt\semantic-corpus'
    $index = Join-Path $Corpus 'openwiki\index.md'
    if (-not (Test-Path $index)) {
        if (-not (Test-Path (Join-Path $prebuilt 'openwiki\index.md'))) {
            Write-Host '    no prebuilt semantic wiki found; run scripts\build-semantic.ps1' -ForegroundColor Yellow
            return
        }
        Write-Step 'Restoring the prebuilt semantic graph into semantic-corpus\'
        New-Item -ItemType Directory -Force -Path $Corpus | Out-Null
        Copy-Item -Path (Join-Path $prebuilt '*') -Destination $Corpus -Recurse -Force
        Get-ChildItem -Path $prebuilt -Force -Filter '.*' | Copy-Item -Destination $Corpus -Recurse -Force
    }
    $isOwnRepo = $false
    if (Test-Path (Join-Path $Corpus '.git')) {
        $top = (& git -C $Corpus rev-parse --show-toplevel 2>$null)
        $isOwnRepo = $top -and ((Resolve-Path $top).Path -eq (Resolve-Path $Corpus).Path)
    }
    if (-not $isOwnRepo) {
        Write-Step 'Making semantic-corpus\ its own git repository (OpenWiki requires this)'
        Initialize-CorpusRepo $Corpus 'corpus (prebuilt semantic wiki)'
    }
}

function Resolve-ProjectPath([string]$PathValue) {
    if ([System.IO.Path]::IsPathRooted($PathValue)) { return $PathValue }
    return [System.IO.Path]::GetFullPath((Join-Path $Script:ProjectRoot $PathValue))
}

function Get-OpenWikiCliJs([hashtable]$EnvValues) {
    # Always launch OpenWiki as `node cli.js` (npm .cmd shims are unreliable from subprocesses).
    $override = $EnvValues['OPENWIKI_CLI_JS']
    if ($override) {
        if (-not (Test-Path $override)) { throw "OPENWIKI_CLI_JS points to a missing file: $override" }
        return (Resolve-Path $override).Path
    }
    $npmRoot = (& npm root -g).Trim()
    $cliJs = Join-Path $npmRoot 'openwiki\dist\cli\cli.js'
    if (-not (Test-Path $cliJs)) { throw "OpenWiki not found at $cliJs. Run scripts\setup.ps1." }
    return $cliJs
}

function Set-OpenWikiEnv([hashtable]$EnvValues) {
    # Applies .env values to this process so child `node cli.js` runs inherit them.
    foreach ($key in $EnvValues.Keys) {
        if ($EnvValues[$key] -ne '') { Set-Item -Path "Env:$key" -Value $EnvValues[$key] }
    }
    $configDir = if ($EnvValues['OPENWIKI_CONFIG_DIR']) { $EnvValues['OPENWIKI_CONFIG_DIR'] } else { '.openwiki-state' }
    $env:OPENWIKI_CONFIG_DIR = Resolve-ProjectPath $configDir
}
