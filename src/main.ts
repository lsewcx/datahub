import { createApp } from 'vue'
import './assets/index.css'
import App from './App.vue'
import router from './router/router'


if (import.meta.env.VITE_USE_MOCK === 'true') {
    import ('./mock/index')
  }

createApp(App).use(router).mount('#app')
