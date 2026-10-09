# Wipe the agent's memory (context-corpus/). Same as the "Reset demo" button in the app.
# If the app is running it asks the backend (which also stops a running sync and restarts the
# memory graph viewer); otherwise it recreates the folder directly.
# Usage (from the project root):  powershell -ExecutionPolicy Bypass -File scripts\reset-context.ps1

. "$PSScriptRoot\common.ps1"
Set-Location $Script:ProjectRoot

$envValues = Read-DotEnv (Join-Path $Script:ProjectRoot '.env')
$backendPort = if ($envValues['BACKEND_PORT']) { $envValues['BACKEND_PORT'] } else { '8000' }
$url = "http://127.0.0.1:$backendPort/api/demo/reset"

$running = $false
try {
    Invoke-RestMethod -Uri "http://127.0.0.1:$backendPort/api/health" -TimeoutSec 3 | Out-Null
    $running = $true
} catch { }

if ($running) {
    Write-Step 'App is running: asking the backend to reset'
    $result = Invoke-RestMethod -Method Post -Uri $url -TimeoutSec 60
    Write-Host "    memory wiped; new session $($result.session_id)" -ForegroundColor Green
} else {
    Write-Step 'App is not running: recreating context-corpus/ directly'
    $venvPython = Join-Path $Script:ProjectRoot '.venv\Scripts\python.exe'
    & $venvPython -c "import sys; sys.path.insert(0, 'backend'); from app.config import Settings; from app.context_store import reset_context_corpus; print('    recreated', reset_context_corpus(Settings()))"
    if ($LASTEXITCODE -ne 0) { throw 'reset failed (is a process still using context-corpus/?)' }
}
