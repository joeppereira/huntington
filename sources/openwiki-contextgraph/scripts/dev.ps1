# Start the backend (which starts both OpenWiki visualizers) and, once it exists, the frontend.
# Usage (from the project root):  powershell -ExecutionPolicy Bypass -File scripts\dev.ps1
# Stop with Ctrl-C; the backend stops its child processes on shutdown.

. "$PSScriptRoot\common.ps1"
Set-Location $Script:ProjectRoot

$envValues = Read-DotEnv (Join-Path $Script:ProjectRoot '.env')
if (-not $envValues['ANTHROPIC_API_KEY']) { throw 'ANTHROPIC_API_KEY is empty in .env.' }
$backendPort = if ($envValues['BACKEND_PORT']) { $envValues['BACKEND_PORT'] } else { '8000' }
$venvPython = Join-Path $Script:ProjectRoot '.venv\Scripts\python.exe'
if (-not (Test-Path $venvPython)) { throw 'No .venv; run scripts\setup.ps1 first.' }

$frontend = $null
if (Test-Path (Join-Path $Script:ProjectRoot 'frontend\package.json')) {
    Write-Step 'Starting frontend (Vite) on http://127.0.0.1:5173'
    # Same console (not Start-Job), so Ctrl-C reaches Vite too; the finally block kills its tree.
    $frontend = Start-Process -FilePath 'npm.cmd' -ArgumentList 'run', 'dev' -NoNewWindow -PassThru `
        -WorkingDirectory (Join-Path $Script:ProjectRoot 'frontend')
}

Write-Step "Starting backend on http://127.0.0.1:$backendPort"
try {
    & $venvPython -m uvicorn app.main:create_app --factory --app-dir backend --host 127.0.0.1 --port $backendPort --timeout-graceful-shutdown 5
} finally {
    if ($frontend -and -not $frontend.HasExited) {
        & taskkill /PID $frontend.Id /T /F *> $null
    }
}
