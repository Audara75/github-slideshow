import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      // String shorthand: '/api' -> 'http://127.0.0.1:5000/api'
      // '/api': 'http://127.0.0.1:5000', // This would also work if paths match exactly

      // With options:
      '/api': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true, // Recommended for virtual hosted sites
        // secure: false, // Uncomment if backend is not on HTTPS and having issues
        // rewrite: (path) => path.replace(/^\/api/, ''), // Use if backend doesn't have /api prefix
                                                       // In our case, backend has /api/ingestion...
                                                       // so we want to keep /api.
      }
    }
  }
})
