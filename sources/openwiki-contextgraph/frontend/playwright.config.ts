import { defineConfig, devices } from '@playwright/test'

// End-to-end tests against the real stack: FastAPI backend (which starts both OpenWiki visualizers)
// plus the Vite dev server. Needs the semantic wiki built and internet (visualizer CDN).
export default defineConfig({
  testDir: './e2e',
  timeout: 60_000,
  fullyParallel: false,
  workers: 1,
  reporter: 'list',
  use: {
    baseURL: 'http://127.0.0.1:5173',
    ...devices['Desktop Chrome'],
  },
  webServer: [
    {
      command:
        '.venv\\Scripts\\python.exe -m uvicorn app.main:create_app --factory --app-dir backend ' +
        '--host 127.0.0.1 --port 8000 --timeout-graceful-shutdown 5',
      cwd: '..',
      // Own memory corpus + manual sync: e2e runs must never wipe the user's context-corpus/
      // (the backend resets its corpus on start) or start a paid OpenWiki sync.
      env: { CONTEXT_CORPUS_DIR: 'logs/e2e-context-corpus', MEMORY_SYNC_MODE: 'manual' },
      url: 'http://127.0.0.1:8000/api/health',
      timeout: 60_000,
      reuseExistingServer: false,
    },
    {
      command: 'npm run dev',
      url: 'http://127.0.0.1:5173',
      timeout: 60_000,
      reuseExistingServer: false,
    },
  ],
})
