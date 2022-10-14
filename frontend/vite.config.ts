import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath } from 'url'

const path = require("path")

// https://vitejs.dev/config/
export default defineConfig({
  build: { manifest: true },
  base: process.env.ELECTRON=="true" ? './' : '/',
  plugins: [ vue({
    template: {
      compilerOptions: {
        isCustomElement: tag => tag.startsWith('box-icon')
      }
    }
  })],
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
      // find: "@", replacement:path.resolve(__dirname,'src')
    },
  },
  server: {
    host: true,
    port: 3000,
    proxy: {
        '/api': {
            target: 'http://127.0.0.1:8000/',
            changeOrigin: false,
            ws: false,
            rewrite: (pathStr) => pathStr.replace('/api', ''),
            timeout: 5000,
        },
    },
  },
})
