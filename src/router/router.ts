
import { createWebHistory, createRouter } from 'vue-router'

import index from '../view/index.vue'

const routes = [
    {
        path: '/',
        component: index
    }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router