<template>
  <div class="dashboard">
    <!-- Statistics Cards -->
    <div class="grid grid-4">
      <div class="stat-card">
        <div class="stat-icon">🏭</div>
        <div class="stat-content">
          <div class="stat-value">{{ statistics?.total_sites || 0 }}</div>
          <div class="stat-label">Total Sites</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">⭐</div>
        <div class="stat-content">
          <div class="stat-value">{{ statistics?.avg_score?.toFixed(1) || '0.0' }}</div>
          <div class="stat-label">Average Score</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">📈</div>
        <div class="stat-content">
          <div class="stat-value">{{ statistics?.max_score?.toFixed(1) || '0.0' }}</div>
          <div class="stat-label">Best Score</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">📉</div>
        <div class="stat-content">
          <div class="stat-value">{{ statistics?.min_score?.toFixed(1) || '0.0' }}</div>
          <div class="stat-label">Lowest Score</div>
        </div>
      </div>
    </div>

    <!-- Main Content Grid -->
    <div class="grid grid-2">
      <!-- Top Sites -->
      <div class="card">
        <div class="card-header">
          <h2>Top 10 Recommended Sites</h2>
          <button @click="exportData" class="btn btn-secondary">Export CSV</button>
        </div>
        <div class="table-container">
          <table class="sites-table">
            <thead>
              <tr>
                <th>Rank</th>
                <th>Site Name</th>
                <th>Region</th>
                <th>Score</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(site, index) in topSites" :key="site.site" class="site-row">
                <td class="rank">{{ index + 1 }}</td>
                <td class="site-name">{{ site.site_name }}</td>
                <td class="region">{{ site.region }}</td>
                <td class="score">
                  <div class="score-badge" :class="getScoreClass(site.total_suitability_score)">
                    {{ formatScore(site.total_suitability_score) }}
                  </div>
                </td>
                <td class="actions">
                  <button @click="viewOnMap(site)" class="btn btn-sm btn-outline">
                    View on Map
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Score Distribution -->
      <div class="card">
        <div class="card-header">
          <h2>Site Suitability Distribution</h2>
        </div>
        <ScoreDistributionChart :distribution="scoreDistribution" />
      </div>
    </div>

    <!-- Quick Filters -->
    <div class="card">
      <h2>Quick Site Filters</h2>
      <div class="filters-grid">
        <div class="filter-group">
          <label>Minimum Score:</label>
          <input
            type="range"
            min="0"
            max="100"
            v-model="filters.min_score"
            @change="updateFilters"
          />
          <span>{{ filters.min_score }}</span>
        </div>
        <div class="filter-group">
          <label>Maximum Score:</label>
          <input
            type="range"
            min="0"
            max="100"
            v-model="filters.max_score"
            @change="updateFilters"
          />
          <span>{{ filters.max_score }}</span>
        </div>
        <div class="filter-group">
          <label>Region:</label>
          <select v-model="filters.region" @change="updateFilters">
            <option value="">All Regions</option>
            <option value="Tamil Nadu">Tamil Nadu</option>
          </select>
        </div>
      </div>
    </div>

    <!-- Site Details Modal -->
    <div v-if="selectedSite" class="modal-overlay" @click="selectedSite = null">
      <div class="modal-content" @click.stop>
        <button class="close-button" @click="selectedSite = null">×</button>
        <SiteDetails :site="selectedSite" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useSitesStore } from '@/stores/sites'
import ScoreDistributionChart from '@/components/charts/ScoreDistributionChart.vue'
import SiteDetails from '@/components/maps/SiteDetails.vue'
import type { AnalysisResult, SiteFilters } from '@/types'

const router = useRouter()
const sitesStore = useSitesStore()

const selectedSite = ref<AnalysisResult | null>(null)
const filters = ref<SiteFilters>({
  min_score: 0,
  max_score: 100,
  region: '',
})

const statistics = computed(() => sitesStore.statistics)
const topSites = computed(() => sitesStore.topSites)
const scoreDistribution = computed(() => sitesStore.scoreDistribution)

const getScoreClass = (score: number) => {
  if (score >= 80) return 'excellent'
  if (score >= 60) return 'good'
  if (score >= 40) return 'fair'
  if (score >= 20) return 'poor'
  return 'very-poor'
}

const updateFilters = () => {
  sitesStore.updateFilters(filters.value)
}

const formatScore = (score: any) => (typeof score === 'number' ? score.toFixed(2) : 'N/A')

const viewOnMap = (site: AnalysisResult) => {
  router.push({
    path: '/map',
    query: { site: site.site.toString() },
  })
}

const exportData = () => {
  sitesStore.exportData('csv')
}

onMounted(() => {
  sitesStore.fetchTopSites(10)
})
</script>

<style scoped>
.dashboard {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.grid-4 {
  grid-template-columns: repeat(4, 1fr);
}

.stat-card {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 1rem;
}

.stat-icon {
  font-size: 2rem;
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 2rem;
  font-weight: bold;
  color: #333;
}

.stat-label {
  color: #666;
  font-size: 0.9rem;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.card-header h2 {
  margin: 0;
  color: #333;
}

.table-container {
  overflow-x: auto;
}

.sites-table {
  width: 100%;
  border-collapse: collapse;
}

.sites-table th {
  background: #f8f9fa;
  padding: 0.75rem;
  text-align: left;
  font-weight: 600;
  color: #555;
  border-bottom: 2px solid #dee2e6;
}

.sites-table td {
  padding: 0.75rem;
  border-bottom: 1px solid #dee2e6;
}

.site-row:hover {
  background: #f8f9fa;
}

.rank {
  font-weight: bold;
  color: #666;
}

.site-name {
  font-weight: 500;
}

.region {
  color: #666;
}

.score-badge {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  border-radius: 20px;
  font-weight: bold;
  font-size: 0.8rem;
  color: white;
}

.score-badge.excellent {
  background: #28a745;
}
.score-badge.good {
  background: #17a2b8;
}
.score-badge.fair {
  background: #ffc107;
  color: #212529;
}
.score-badge.poor {
  background: #fd7e14;
}
.score-badge.very-poor {
  background: #dc3545;
}

.filters-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.filter-group label {
  font-weight: 500;
  color: #555;
}

.filter-group input[type='range'] {
  width: 100%;
}

.filter-group select {
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  background: white;
}

.btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.3s ease;
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background: #545b62;
}

.btn-sm {
  padding: 0.25rem 0.5rem;
  font-size: 0.8rem;
}

.btn-outline {
  background: transparent;
  border: 1px solid #007bff;
  color: #007bff;
}

.btn-outline:hover {
  background: #007bff;
  color: white;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 20px;
  border-radius: 8px;
  max-width: 500px;
  width: 90%;
  max-height: 80vh;
  overflow-y: auto;
  position: relative;
}

.close-button {
  position: absolute;
  top: 10px;
  right: 10px;
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #666;
}

.close-button:hover {
  color: #333;
}

@media (max-width: 1024px) {
  .grid-4 {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .grid-4 {
    grid-template-columns: 1fr;
  }

  .card-header {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }
}
</style>
