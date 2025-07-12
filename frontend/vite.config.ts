import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
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
  },
})
