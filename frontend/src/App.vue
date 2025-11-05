<template>
  <div id="app">
    <header class="app-header">
      <div class="container">
        <h1>🌞 Solar Site Analyzer</h1>
        <nav>
          <router-link to="/">Dashboard</router-link>
          <router-link to="/map">Interactive Map</router-link>
          <router-link to="/analysis">Site Analysis</router-link>
        </nav>
      </div>
    </header>

    <main class="app-main">
      <div class="container">
        <router-view />
      </div>
    </main>

    <footer class="app-footer">
      <div class="container">
        <p>&copy; 2024 Solar Site Analyzer - Datasee.AI Assessment</p>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import { useSitesStore } from '@/stores/sites';

const sitesStore = useSitesStore();

onMounted(() => {
  sitesStore.fetchSites();
  sitesStore.fetchStatistics();
});
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  line-height: 1.6;
  color: #333;
  background-color: #f8f9fa;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.app-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 1rem 0;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.app-header .container {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.app-header h1 {
  font-size: 1.8rem;
  font-weight: 600;
}

.app-header nav {
  display: flex;
  gap: 2rem;
}

.app-header nav a {
  color: white;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: background-color 0.3s ease;
}

.app-header nav a:hover,
.app-header nav a.router-link-active {
  background-color: rgba(255, 255, 255, 0.2);
}

.app-main {
  min-height: calc(100vh - 140px);
  padding: 2rem 0;
}

.app-footer {
  background: #343a40;
  color: white;
  text-align: center;
  padding: 1rem 0;
  margin-top: 2rem;
}

/* Utility classes */
.card {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  margin-bottom: 1.5rem;
}

.grid {
  display: grid;
  gap: 1.5rem;
}

.grid-2 {
  grid-template-columns: 1fr 1fr;
}

.grid-3 {
  grid-template-columns: 1fr 1fr 1fr;
}

@media (max-width: 768px) {
  .grid-2,
  .grid-3 {
    grid-template-columns: 1fr;
  }
  
  .app-header .container {
    flex-direction: column;
    gap: 1rem;
  }
  
  .app-header nav {
    gap: 1rem;
  }
}
</style>