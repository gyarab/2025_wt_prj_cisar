


import {createRouter, createWebHistory} from 'vue-router'
import Teams from '../views/Teams.vue'
import Players from '../views/Players.vue'

const router = createRouter({
    history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Teams
    },
    {
      path: '/about',
      name: 'About',
      component: Players
    }
  ]
})
export default router