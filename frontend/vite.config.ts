import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  base: '/static/',
  plugins: [react()],
  server: {
    // Enable HMR
    hmr: true,
    // Watch for changes in these directories
    watch: {
      usePolling: true,
    },
    // Host settings for better network access
    host: true,
    // Proxy API requests to the backend for development
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
})