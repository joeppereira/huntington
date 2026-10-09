# Milestone 2: build the Stage 1 semantic wiki with OpenWiki.
# Usage (from the project root):
#   powershell -ExecutionPolicy Bypass -File scripts\build-semantic.ps1                 # model from .env
#   powershell -ExecutionPolicy Bypass -File scripts\build-semantic.ps1 -ModelId claude-haiku-4-5-20251001
#   powershell -ExecutionPolicy Bypass -File scripts\build-semantic.ps1 -SkipInit       # corpus + git only

param(
    [string]$ModelId = '',
    [switch]$SkipInit
)

. "$PSScriptRoot\common.ps1"
Set-Location $Script:ProjectRoot

$envValues = Read-DotEnv (Join-Path $Script:ProjectRoot '.env')
if (-not $envValues['ANTHROPIC_API_KEY']) { throw 'ANTHROPIC_API_KEY is empty in .env.' }
Set-OpenWikiEnv $envValues
if ($ModelId) { $env:OPENWIKI_MODEL_ID = $ModelId }

$cliJs = Get-OpenWikiCliJs $envValues
$venvPython = Join-Path $Script:ProjectRoot '.venv\Scripts\python.exe'
$corpusName = if ($envValues['SEMANTIC_CORPUS_DIR']) { $envValues['SEMANTIC_CORPUS_DIR'] } else { 'semantic-corpus' }
$corpus = Resolve-ProjectPath $corpusName
$logDir = Join-Path $Script:ProjectRoot 'logs'
New-Item -ItemType Directory -Force -Path $logDir, $env:OPENWIKI_CONFIG_DIR | Out-Null

Write-Step "Converting data/ into $corpus"
& $venvPython (Join-Path $Script:ProjectRoot 'tools\convert_corpus.py') --data data --out $corpus
if ($LASTEXITCODE -ne 0) { throw 'convert_corpus.py failed.' }

Write-Step 'Writing .openwikiignore and INSTRUCTIONS.md brief'
Write-Utf8NoBom (Join-Path $corpus '.openwikiignore') "raw/`n"
New-Item -ItemType Directory -Force -Path (Join-Path $corpus 'openwiki') | Out-Null
$brief = Join-Path $corpus 'openwiki\INSTRUCTIONS.md'
Copy-Item (Join-Path $Script:ProjectRoot 'templates\semantic-INSTRUCTIONS.md') $brief -Force

Write-Step 'Committing corpus as its own git repo'
Push-Location $corpus
try {
    if (-not (Test-Path '.git')) { & git init --quiet }
    # Keep bytes as-is: global autocrlf would otherwise treat the raw PDFs as text.
    & git config core.autocrlf false
    if (-not (& git config user.email)) {
        & git config user.email 'poc@openwiki.local'
        & git config user.name 'OpenWiki POC'
    }
    & git add -A
    & git diff --cached --quiet
    if ($LASTEXITCODE -ne 0) {
        & git commit --quiet -m 'corpus'
        if ($LASTEXITCODE -ne 0) { throw 'git commit failed in corpus.' }
    }
    Write-Host "    $(& git log --oneline -1)"
} finally { Pop-Location }

if ($SkipInit) { Write-Host 'Skipping OpenWiki init (-SkipInit).'; return }

Initialize-OpenWikiOnboarding $env:OPENWIKI_CONFIG_DIR

$stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$log = Join-Path $logDir "semantic-init-$stamp.log"
Write-Step "Running OpenWiki --init with $env:OPENWIKI_MODEL_ID (log: $log)"
Write-Host '    Expect tens of minutes. Interrupted runs resume from openwiki/.run.json.'
$briefHash = (Get-FileHash $brief).Hash
Push-Location $corpus
try {
    $ErrorActionPreference = 'Continue'
    & node $cliJs --init --print *>&1 | Tee-Object -FilePath $log
    $exitCode = $LASTEXITCODE
    $ErrorActionPreference = 'Stop'
} finally { Pop-Location }
if ($exitCode -ne 0) { throw "openwiki --init failed (exit $exitCode). See $log" }
if ((Get-FileHash $brief).Hash -ne $briefHash) { Write-Warning 'INSTRUCTIONS.md changed during init.' }

$wikiDir = Join-Path $corpus 'openwiki'
# Page workers that fail or never submit leave silent stubs (openwiki_generated: true). A plain
# --update plans nothing when sources are unchanged, so name the stubs in the update message.
$stubs = @(Get-ChildItem $wikiDir -Recurse -Filter '*.md' |
    Where-Object { Select-String -Path $_.FullName -Pattern '^openwiki_generated:\s*true' -Quiet } |
    ForEach-Object { '/openwiki/' + $_.FullName.Substring($wikiDir.Length + 1).Replace('\', '/') })
if ($stubs.Count -gt 0) {
    $updateLog = Join-Path $logDir "semantic-update-$stamp.log"
    Write-Step "Re-running $($stubs.Count) skipped page(s) with --update (log: $updateLog)"
    $message = "Required page edits: these $($stubs.Count) pages were skipped during init and are still " +
        'placeholder stubs (openwiki_generated: true, no description, type Reference). Plan all of them ' +
        'for a full rewrite following openwiki/INSTRUCTIONS.md (correct front-matter type from the brief, ' +
        "description, content, Relationships section with links): $($stubs -join ', '). Do not change other pages."
    Push-Location $corpus
    try {
        $ErrorActionPreference = 'Continue'
        & node $cliJs --update --print $message *>&1 | Tee-Object -FilePath $updateLog
        $exitCode = $LASTEXITCODE
        $ErrorActionPreference = 'Stop'
    } finally { Pop-Location }
    if ($exitCode -ne 0) { throw "openwiki --update failed (exit $exitCode). See $updateLog" }
}

Write-Step 'Verifying generated wiki'
$pages = @(Get-ChildItem $wikiDir -Recurse -Filter '*.md' |
    Where-Object { $_.FullName -notmatch '\\\.claims\\' -and $_.Name -notin @('INSTRUCTIONS.md', 'log.md') })
$index = Join-Path $wikiDir 'index.md'
$remaining = @($pages | Where-Object { Select-String -Path $_.FullName -Pattern '^openwiki_generated:\s*true' -Quiet })
if ($remaining.Count -gt 0) { Write-Warning "$($remaining.Count) page(s) are still stubs; run `openwiki --update --print `"<message naming them>`"` in the corpus (see docs/openwiki-findings.md)." }
$types = $pages | ForEach-Object {
    $match = Select-String -Path $_.FullName -Pattern '^type:\s*(.+)$' | Select-Object -First 1
    if ($match) { $match.Matches[0].Groups[1].Value.Trim('"', "'", ' ') } else { '(none)' }
} | Group-Object | Sort-Object Count -Descending
Write-Host "    pages: $($pages.Count)"
Write-Host "    index.md: $(if (Test-Path $index) { 'present' } else { 'MISSING' })"
Write-Host "    .claims/: $(if (Test-Path (Join-Path $wikiDir '.claims')) { 'present' } else { 'missing' })"
$types | ForEach-Object { Write-Host ("    type {0,-22} {1}" -f $_.Name, $_.Count) }
Write-Host ''
Write-Host "View it: node `"$cliJs`" visualize `"$wikiDir`" --no-open" -ForegroundColor Green
