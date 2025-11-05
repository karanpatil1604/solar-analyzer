import { createRouter, createWebHistory } from 'vue-router';
import Dashboard from '@/views/Dashboard.vue';
import MapView from '@/views/MapView.vue';
import AnalysisView from '@/views/AnalysisView.vue';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'Dashboard',
      component: Dashboard
    },
    {
      path: '/map',
      name: 'Map',
      component: MapView
    },
    {
      path: '/analysis',
      name: 'Analysis',
      component: AnalysisView
    }
  ]
});

export default router;