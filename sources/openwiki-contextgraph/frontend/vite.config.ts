import react from '@vitejs/plugin-react'
import path from 'node:path'
import { defineConfig, loadEnv } from 'vite'

// The project .env (one level up) holds BACKEND_PORT; /api is proxied there so the app never
// hard-codes the backend URL. Vite must listen on 127.0.0.1:5173 to match FRONTEND_ORIGIN (CORS).
const projectEnv = loadEnv('development', path.resolve(__dirname, '..'), '')
const backendPort = projectEnv.BACKEND_PORT || '8000'

export default defineConfig({
  plugins: [react()],
  server: {
    host: '127.0.0.1',
    port: 5173,
    strictPort: true,
    proxy: {
      '/api': `http://127.0.0.1:${backendPort}`,
    },
  },
})
