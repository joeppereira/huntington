# Milestone 1: check prerequisites, install OpenWiki, create the Python venv, prepare .env.
# Usage (from the project root):  powershell -ExecutionPolicy Bypass -File scripts\setup.ps1

. "$PSScriptRoot\common.ps1"
Set-Location $Script:ProjectRoot

function Assert-Command([string]$Name, [string]$Hint) {
    if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) { throw "$Name not found on PATH. $Hint" }
}

Write-Step 'Checking prerequisites'
Assert-Command 'node' 'Install Node.js 22.22.0 or newer.'
Assert-Command 'npm' 'npm ships with Node.js.'
Assert-Command 'git' 'Install Git for Windows.'

$nodeVersion = [version]((& node --version).TrimStart('v'))
if ($nodeVersion -lt [version]'22.22.0') { throw "Node $nodeVersion is too old; OpenWiki needs 22.22.0+." }
Write-Host "    node $nodeVersion, $(& git --version)"

# Prefer Python 3.13/3.12 via the py launcher: some dependencies lack wheels for 3.14.
$pythonCmd = $null
foreach ($candidate in @('3.13', '3.12')) {
    if (Get-Command 'py' -ErrorAction SilentlyContinue) {
        & py "-$candidate" --version *> $null
        if ($LASTEXITCODE -eq 0) { $pythonCmd = @('py', "-$candidate"); break }
    }
}
if (-not $pythonCmd) {
    Assert-Command 'python' 'Install Python 3.12 or 3.13.'
    $pyVersion = [version]((& python -c "import sys; print('.'.join(map(str, sys.version_info[:2])))").Trim())
    if ($pyVersion -lt [version]'3.12' -or $pyVersion -ge [version]'3.14') {
        throw "Python $pyVersion found; install 3.12 or 3.13."
    }
    $pythonCmd = @('python')
}
Write-Host "    python: $($pythonCmd -join ' ')"

Write-Step "Installing OpenWiki $Script:OpenWikiVersion (npm, not bun)"
$installed = (& npm ls -g openwiki --depth=0 --json 2>$null | ConvertFrom-Json).dependencies.openwiki.version
if ($installed -eq $Script:OpenWikiVersion) {
    Write-Host "    already installed"
} else {
    & npm install -g "openwiki@$Script:OpenWikiVersion"
    if ($LASTEXITCODE -ne 0) { throw 'npm install -g openwiki failed.' }
}

$envValues = Read-DotEnv (Join-Path $Script:ProjectRoot '.env')
$cliJs = Get-OpenWikiCliJs $envValues
$sqliteBinary = Join-Path (Split-Path (Split-Path (Split-Path $cliJs))) 'node_modules\better-sqlite3\build\Release\better_sqlite3.node'
if (-not (Test-Path $sqliteBinary)) {
    throw "better-sqlite3 native binary missing ($sqliteBinary). Run: npm approve-scripts better-sqlite3; then npm rebuild -g openwiki"
}
Write-Host "    cli.js: $cliJs"

Write-Step 'Creating Python venv (.venv) and installing requirements'
$venvPython = Join-Path $Script:ProjectRoot '.venv\Scripts\python.exe'
if (Test-Path $venvPython) {
    # A .venv copied from another machine points at that machine's Python; rebuild it.
    & $venvPython -c "import sys" *> $null
    if ($LASTEXITCODE -ne 0) {
        Write-Host '    existing .venv does not work on this machine; recreating it'
        Remove-Item -Recurse -Force (Join-Path $Script:ProjectRoot '.venv')
    }
}
if (-not (Test-Path $venvPython)) {
    $pyExe = $pythonCmd[0]
    $pyArgs = @($pythonCmd | Select-Object -Skip 1) + @('-m', 'venv', '.venv')
    & $pyExe @pyArgs
    if ($LASTEXITCODE -ne 0) { throw 'venv creation failed.' }
}
& $venvPython -m pip install --quiet --upgrade pip
& $venvPython -m pip install --quiet -r (Join-Path $Script:ProjectRoot 'backend\requirements.txt')
if ($LASTEXITCODE -ne 0) { throw 'pip install failed.' }

$frontendPackage = Join-Path $Script:ProjectRoot 'frontend\package.json'
if (Test-Path $frontendPackage) {
    Write-Step 'Installing frontend dependencies'
    Push-Location (Join-Path $Script:ProjectRoot 'frontend')
    try {
        & npm install
        if ($LASTEXITCODE -ne 0) { throw 'npm install (frontend) failed.' }
    } finally { Pop-Location }
}

Write-Step 'Preparing .env, state and log folders'
$envPath = Join-Path $Script:ProjectRoot '.env'
if (-not (Test-Path $envPath)) {
    Copy-Item (Join-Path $Script:ProjectRoot '.env.example') $envPath
    Write-Host '    created .env from .env.example (add your ANTHROPIC_API_KEY)'
}
foreach ($dir in @('.openwiki-state', 'logs')) {
    New-Item -ItemType Directory -Force -Path (Join-Path $Script:ProjectRoot $dir) | Out-Null
}
$envValues = Read-DotEnv $envPath
$configDir = if ($envValues['OPENWIKI_CONFIG_DIR']) { $envValues['OPENWIKI_CONFIG_DIR'] } else { '.openwiki-state' }
Initialize-OpenWikiOnboarding (Resolve-ProjectPath $configDir)
$semanticDir = if ($envValues['SEMANTIC_CORPUS_DIR']) { $envValues['SEMANTIC_CORPUS_DIR'] } else { 'semantic-corpus' }
Restore-SemanticCorpus (Resolve-ProjectPath $semanticDir)

if (-not (Test-Path (Join-Path $Script:ProjectRoot '.git'))) {
    Write-Step 'Initialising project git repo'
    & git init --quiet $Script:ProjectRoot
}

$envValues = Read-DotEnv $envPath
if (-not $envValues['ANTHROPIC_API_KEY']) {
    Write-Host ''
    Write-Host 'Setup complete. Next: put your ANTHROPIC_API_KEY in .env, then run scripts\dev.ps1.' -ForegroundColor Yellow
} else {
    Write-Host ''
    Write-Host 'Setup complete. Next: run scripts\dev.ps1.' -ForegroundColor Green
}
