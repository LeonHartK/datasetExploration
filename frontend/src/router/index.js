import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../views/Dashboard.vue'
import TemporalAnalysis from '../views/TemporalAnalysis.vue'
import CustomerAnalysis from '../views/CustomerAnalysis.vue'
import ProductAnalysis from '../views/ProductAnalysis.vue'
import Recommendations from '../views/Recommendations.vue'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard
  },
  {
    path: '/temporal',
    name: 'TemporalAnalysis',
    component: TemporalAnalysis
  },
  {
    path: '/customers',
    name: 'CustomerAnalysis',
    component: CustomerAnalysis
  },
  {
    path: '/products',
    name: 'ProductAnalysis',
    component: ProductAnalysis
  },
  {
    path: '/recommendations',
    name: 'Recommendations',
    component: Recommendations
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
