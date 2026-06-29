import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Hosts allowed to reach the dev server (Vite blocks unknown Host headers).
// Set VITE_ALLOWED_HOSTS in the environment, comma-separated, e.g.
//   VITE_ALLOWED_HOSTS=submitflow.tramuntana.dev
// or VITE_ALLOWED_HOSTS=all to disable the check entirely.
const envHosts = (process.env.VITE_ALLOWED_HOSTS || '').trim()
const allowedHosts =
  envHosts === 'all'
    ? true
    : ['localhost', '127.0.0.1', ...envHosts.split(',').map((h) => h.trim()).filter(Boolean)]

export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 3000,
    watch: { usePolling: true }, // reliable hot-reload inside Docker
    allowedHosts,
    // Proxy API calls to the backend so a relative VITE_API_URL (/api/v1)
    // works both behind nginx and when hitting the dev server directly.
    proxy: {
      '/api': {
        target: process.env.VITE_PROXY_TARGET || 'http://backend:8000',
        changeOrigin: true,
      },
    },
  },
})
