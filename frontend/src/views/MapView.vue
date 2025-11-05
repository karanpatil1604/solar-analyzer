<template>
  <div class="map-view">
    <div class="map-header">
      <h1>Interactive Site Map</h1>
      <div class="map-controls">
        <div class="filter-group">
          <label>Score Range:</label>
          <div class="range-inputs">
            <input
              type="number"
              v-model="filters.min_score"
              min="0"
              max="100"
              placeholder="Min"
              @change="updateMap"
            />
            <span>to</span>
            <input
              type="number"
              v-model="filters.max_score"
              min="0"
              max="100"
              placeholder="Max"
              @change="updateMap"
            />
          </div>
        </div>
        <div class="legend">
          <div class="legend-item">
            <div class="legend-color excellent"></div>
            <span>Excellent (80-100)</span>
          </div>
          <div class="legend-item">
            <div class="legend-color good"></div>
            <span>Good (60-79)</span>
          </div>
          <div class="legend-item">
            <div class="legend-color fair"></div>
            <span>Fair (40-59)</span>
          </div>
          <div class="legend-item">
            <div class="legend-color poor"></div>
            <span>Poor (20-39)</span>
          </div>
          <div class="legend-item">
            <div class="legend-color very-poor"></div>
            <span>Very Poor (0-19)</span>
          </div>
        </div>
      </div>
    </div>

    <div class="map-container">
      <SiteMap
        v-if="filteredSites && filteredSites.length"
        :key="filteredSites.length + '-' + route.query.site"
        :sites="filteredSites"
        :loading="loading"
        @site-selected="onSiteSelected"
      />
    </div>

    <!-- Selected Site Panel -->
    <div v-if="selectedSite" class="side-panel">
      <div class="panel-header">
        <h3>Site Details</h3>
        <button @click="selectedSite = null" class="close-panel">×</button>
      </div>
      <SiteDetails :site="selectedSite" />
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-overlay">
      <div class="loading-spinner"></div>
      <p>Loading sites...</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useSitesStore } from '@/stores/sites'
import SiteMap from '@/components/maps/SiteMap.vue'
import SiteDetails from '@/components/maps/SiteDetails.vue'
import type { AnalysisResult, SiteFilters } from '@/types'

const route = useRoute()
const router = useRouter()
const sitesStore = useSitesStore()

const selectedSite = ref<AnalysisResult | null>(null)
const filters = ref<SiteFilters>({
  min_score: 0,
  max_score: 100,
})

const filteredSites = computed(() => sitesStore.filteredSites)
const loading = computed(() => sitesStore.loading)

const updateMap = () => {
  sitesStore.updateFilters(filters.value)
}

const onSiteSelected = (site: AnalysisResult) => {
  if (!site.latitude || !site.longitude) return
  selectedSite.value = site
  // Update URL without navigation
  router.replace({
    query: { ...route.query, site: site.site.toString() },
  })
}

// Handle URL parameters
onMounted(() => {
  sitesStore.fetchSites()

  // Check for site ID in URL
  if (route.query.site) {
    const siteId = parseInt(route.query.site as string)
    const site = sitesStore.analysisResults.find((s) => s.site === siteId)
    if (site) {
      selectedSite.value = site
    }
  }
})

// Watch for filter changes
watch(filters, updateMap, { deep: true })
</script>

<style scoped>
.map-view {
  position: relative;
  height: calc(100vh - 200px);
  display: flex;
  flex-direction: column;
}

.map-header {
  background: white;
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 1rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.map-header h1 {
  margin: 0 0 1rem 0;
  color: #333;
}

.map-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.filter-group label {
  font-weight: 500;
  color: #555;
}

.range-inputs {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.range-inputs input {
  width: 80px;
  padding: 0.25rem 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.legend {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.8rem;
}

.legend-color {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  border: 2px solid white;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
}

.legend-color.excellent {
  background: #28a745;
}
.legend-color.good {
  background: #17a2b8;
}
.legend-color.fair {
  background: #ffc107;
}
.legend-color.poor {
  background: #fd7e14;
}
.legend-color.very-poor {
  background: #dc3545;
}

.map-container {
  flex: 1;
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  position: relative;
}

.side-panel {
  position: fixed;
  top: 0;
  right: 0;
  bottom: 0;
  width: 400px;
  background: white;
  box-shadow: -2px 0 10px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  overflow-y: auto;
  transform: translateX(100%);
  transition: transform 0.3s ease;
}

.side-panel[style*='display: block'] {
  transform: translateX(0);
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border-bottom: 1px solid #eee;
  background: #f8f9fa;
}

.panel-header h3 {
  margin: 0;
  color: #333;
}

.close-panel {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #666;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-panel:hover {
  color: #333;
}

.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.9);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 1001;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #007bff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

@media (max-width: 768px) {
  .map-controls {
    flex-direction: column;
    align-items: flex-start;
  }

  .legend {
    justify-content: flex-start;
  }

  .side-panel {
    width: 100%;
  }
}
</style>
