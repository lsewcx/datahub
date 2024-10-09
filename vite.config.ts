import { defineConfig } from 'vite'
import { fileURLToPath } from 'url';
import vue from '@vitejs/plugin-vue'
import tailwind from 'tailwindcss'
import autoprefixer from 'autoprefixer'
import dotenv from 'dotenv'
import path from 'node:path'
import AutoImport from "unplugin-auto-import/vite";
dotenv.config()
const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)
// https://vitejs.dev/config/
export default defineConfig({
  css: {
    postcss: {
      plugins: [tailwind(), autoprefixer(),
      ],
    },
  },
  plugins: [vue(), AutoImport({
    imports: [
      'vue', // 自动导入 Vue 相关函数，如 ref, reactive 等
      'vue-router', // 自动导入 Vue Router 相关函数
      '@vueuse/core', // 自动导入 VueUse 库

    ],
    dts: 'src/auto-imports.d.ts', // 生成的类型声明文件路径
    eslintrc: {
      enabled: true, // 生成 ESLint 配置文件
      filepath: './.eslintrc-auto-import.json', // ESLint 配置文件路径
      globalsPropValue: true, // 全局变量的值
    },
  }),],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, process.env.VITE_ALIAS_SRC || './src'),
    },
  },

})
