<template>
  <div class="analysis-view">
    <h1>Site Suitability Analysis</h1>

    <div class="grid grid-2">
      <!-- Custom Analysis Form -->
      <div class="card">
        <h2>Custom Suitability Analysis</h2>
        <form @submit.prevent="calculateCustomSuitability" class="analysis-form">
          <div class="form-grid">
            <div class="form-group">
              <label>Solar Irradiance (kWh/m²/day):</label>
              <input
                type="number"
                v-model="customAnalysis.solar_irradiance_kwh"
                step="0.1"
                min="0"
                max="10"
                required
              />
            </div>
            <div class="form-group">
              <label>Area (m²):</label>
              <input type="number" v-model="customAnalysis.area_sqm" min="0" required />
            </div>
            <div class="form-group">
              <label>Grid Distance (km):</label>
              <input
                type="number"
                v-model="customAnalysis.grid_distance_km"
                step="0.1"
                min="0"
                required
              />
            </div>
            <div class="form-group">
              <label>Slope (degrees):</label>
              <input
                type="number"
                v-model="customAnalysis.slope_degrees"
                step="0.1"
                min="0"
                max="90"
                required
              />
            </div>
            <div class="form-group">
              <label>Road Distance (km):</label>
              <input
                type="number"
                v-model="customAnalysis.road_distance_km"
                step="0.1"
                min="0"
                required
              />
            </div>
          </div>

          <div class="weights-section">
            <h3>Adjust Weights</h3>
            <div class="weights-grid">
              <div class="weight-group" v-for="weight in weightControls" :key="weight.key">
                <label>{{ weight.label }}:</label>
                <input
                  type="range"
                  v-model="customAnalysis[weight.key]"
                  min="0"
                  max="1"
                  step="0.05"
                  @input="updateWeights"
                />
                <span>{{ (customAnalysis[weight.key] * 100).toFixed(0) }}%</span>
              </div>
            </div>
            <div class="weights-total">
              Total: {{ totalWeight }}%
              <span v-if="totalWeight !== 100" class="error-text"> (Must equal 100%)</span>
            </div>
          </div>

          <button type="submit" class="btn btn-primary" :disabled="loading || totalWeight !== 100">
            {{ loading ? 'Calculating...' : 'Calculate Suitability' }}
          </button>
        </form>
      </div>

      <!-- Results Display -->
      <div class="card">
        <h2>Analysis Results</h2>
        <div v-if="analysisResult" class="results-container">
          <div class="total-score-section">
            <div class="total-score" :class="getScoreClass(analysisResult.total_score)">
              {{ analysisResult.total_score.toFixed(1) }}
            </div>
            <div class="score-label">Overall Suitability Score</div>
          </div>

          <div class="breakdown-section">
            <h3>Score Breakdown</h3>
            <div class="breakdown-grid">
              <div
                v-for="(score, factor) in analysisResult.breakdown"
                :key="factor"
                class="breakdown-item"
              >
                <div class="factor-name">{{ formatFactorName(factor) }}</div>
                <div class="score-bar">
                  <div
                    class="score-fill"
                    :style="{ width: score + '%' }"
                    :class="getScoreClass(score)"
                  ></div>
                </div>
                <div class="score-value">{{ score.toFixed(1) }}</div>
              </div>
            </div>
          </div>

          <div class="weights-used">
            <h3>Weights Used</h3>
            <div class="weights-list">
              <div
                v-for="(weight, key) in analysisResult.weights_used"
                :key="key"
                class="weight-item"
              >
                <span class="weight-label">{{ formatFactorName(key) }}:</span>
                <span class="weight-value">{{ (weight * 100).toFixed(0) }}%</span>
              </div>
            </div>
          </div>
        </div>

        <div v-else class="no-results">
          <p>Enter site parameters and click "Calculate Suitability" to see results.</p>
        </div>
      </div>
    </div>

    <!-- Comparison Section -->
    <div class="card">
      <h2>Site Comparison</h2>
      <div class="comparison-controls">
        <select v-model="selectedSite1" @change="updateComparison">
          <option value="">Select first site...</option>
          <option
            v-for="site in sitesStore.analysisResults"
            :key="site.site"
            :value="site.site"
          >
            {{ site.site_name }} ({{ formatScore(site.total_suitability_score) }})
          </option>
        </select>
        <select v-model="selectedSite2" @change="updateComparison">
          <option value="">Select second site...</option>
          <option
            v-for="site in sitesStore.analysisResults"
            :key="site.site"
            :value="site.site"
          >
            {{ site.site_name }} ({{ formatScore(site.total_suitability_score) }})
          </option>
        </select>
      </div>

      <div v-if="comparisonSites.length === 2" class="comparison-results">
        <div class="comparison-grid">
          <div class="comparison-header">
            <div>Factor</div>
            <div>{{ comparisonSites[0].site_name }}</div>
            <div>{{ comparisonSites[1].site_name }}</div>
          </div>

          <div class="comparison-row" v-for="factor in comparisonFactors" :key="factor.key">
            <div class="factor-name">{{ factor.name }}</div>
            <div class="factor-value">
              {{ getSiteFactorValue(comparisonSites[0], factor.key) }}
            </div>
            <div class="factor-value">
              {{ getSiteFactorValue(comparisonSites[1], factor.key) }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useSitesStore } from '@/stores/sites'
import type { AnalysisResult } from '@/types'

const sitesStore = useSitesStore()

const customAnalysis = ref({
  solar_irradiance_kwh: 5.5,
  area_sqm: 50000,
  grid_distance_km: 1.0,
  slope_degrees: 2.0,
  road_distance_km: 0.5,
  solar_weight: 0.35,
  area_weight: 0.25,
  grid_weight: 0.2,
  slope_weight: 0.15,
  infra_weight: 0.05,
})

const analysisResult = ref<any>(null)
const loading = ref(false)
const selectedSite1 = ref<number | null>(null)
const selectedSite2 = ref<number | null>(null)
const comparisonSites = ref<AnalysisResult[]>([])

const weightControls = [
  { key: 'solar_weight', label: 'Solar Irradiance' },
  { key: 'area_weight', label: 'Area' },
  { key: 'grid_weight', label: 'Grid Distance' },
  { key: 'slope_weight', label: 'Slope' },
  { key: 'infra_weight', label: 'Infrastructure' },
]

const comparisonFactors = [
  { key: 'total_suitability_score', name: 'Total Score' },
  { key: 'solar_irradiance_score', name: 'Solar Score' },
  { key: 'area_score', name: 'Area Score' },
  { key: 'grid_distance_score', name: 'Grid Score' },
  { key: 'slope_score', name: 'Slope Score' },
  { key: 'infrastructure_score', name: 'Infrastructure Score' },
]

const totalWeight = computed(() => {
  const total = weightControls.reduce((sum, weight) => {
    return (
      sum + (customAnalysis.value[weight.key as keyof typeof customAnalysis.value] as number) * 100
    )
  }, 0)
  return Math.round(total)
})
const formatScore = (score: any) => (typeof score === 'number' ? score.toFixed(2) : 'N/A')
const updateWeights = () => {
  // Normalize weights if total is not 100%
  if (totalWeight.value !== 100) {
    const scale = 100 / totalWeight.value
    weightControls.forEach((weight) => {
      const current = customAnalysis.value[
        weight.key as keyof typeof customAnalysis.value
      ] as number
      customAnalysis.value[weight.key as keyof typeof customAnalysis.value] = current * scale
    })
  }
}

const calculateCustomSuitability = async () => {
  if (totalWeight.value !== 100) {
    alert('Weights must total 100%')
    return
  }

  loading.value = true
  try {
    const result = await sitesStore.calculateCustomSuitability(customAnalysis.value, {
      solar_weight: customAnalysis.value.solar_weight,
      area_weight: customAnalysis.value.area_weight,
      grid_weight: customAnalysis.value.grid_weight,
      slope_weight: customAnalysis.value.slope_weight,
      infra_weight: customAnalysis.value.infra_weight,
    })
    analysisResult.value = result
  } catch (error) {
    console.error('Calculation failed:', error)
  } finally {
    loading.value = false
  }
}

const getScoreClass = (score: number) => {
  if (score >= 80) return 'excellent'
  if (score >= 60) return 'good'
  if (score >= 40) return 'fair'
  if (score >= 20) return 'poor'
  return 'very-poor'
}

const formatFactorName = (factor: string) => {
  const names: { [key: string]: string } = {
    solar: 'Solar Irradiance',
    area: 'Area',
    grid: 'Grid Distance',
    slope: 'Slope',
    infrastructure: 'Infrastructure',
  }
  return names[factor] || factor
}

const updateComparison = () => {
  comparisonSites.value = []

  if (selectedSite1.value) {
    const site1 = sitesStore.analysisResults.find((s) => s.site === selectedSite1.value)
    if (site1) comparisonSites.value.push(site1)
  }

  if (selectedSite2.value) {
    const site2 = sitesStore.analysisResults.find((s) => s.site === selectedSite2.value)
    if (site2) comparisonSites.value.push(site2)
  }
}

const getSiteFactorValue = (site: AnalysisResult, factor: string) => {
  const value = (site as any)[factor]
  return typeof value === 'number' ? value.toFixed(1) : value
}

onMounted(() => {
  sitesStore.fetchSites()
})
</script>

<style scoped>
.analysis-view {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.analysis-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-weight: 500;
  color: #555;
}

.form-group input {
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  background: white;
}

.weights-section {
  border: 1px solid #e9ecef;
  padding: 1rem;
  border-radius: 4px;
  background: #f8f9fa;
}

.weights-section h3 {
  margin: 0 0 1rem 0;
  color: #333;
}

.weights-grid {
  display: grid;
  gap: 0.75rem;
}

.weight-group {
  display: grid;
  grid-template-columns: 1fr 2fr auto;
  align-items: center;
  gap: 0.5rem;
}

.weight-group label {
  font-weight: 500;
  color: #555;
}

.weights-total {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #dee2e6;
  font-weight: bold;
  text-align: center;
}

.error-text {
  color: #dc3545;
  font-size: 0.9rem;
}

.btn-primary {
  background: #007bff;
  color: white;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s ease;
}

.btn-primary:hover:not(:disabled) {
  background: #0056b3;
}

.btn-primary:disabled {
  background: #6c757d;
  cursor: not-allowed;
}

.results-container {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.total-score-section {
  text-align: center;
  padding: 2rem;
  background: #f8f9fa;
  border-radius: 8px;
}

.total-score {
  font-size: 3rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
}

.total-score.excellent {
  color: #28a745;
}
.total-score.good {
  color: #17a2b8;
}
.total-score.fair {
  color: #ffc107;
}
.total-score.poor {
  color: #fd7e14;
}
.total-score.very-poor {
  color: #dc3545;
}

.score-label {
  color: #666;
  font-size: 1.1rem;
}

.breakdown-grid {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.breakdown-item {
  display: grid;
  grid-template-columns: 1fr 2fr auto;
  align-items: center;
  gap: 1rem;
}

.factor-name {
  font-weight: 500;
  color: #555;
}

.score-bar {
  height: 20px;
  background: #e9ecef;
  border-radius: 10px;
  overflow: hidden;
}

.score-fill {
  height: 100%;
  border-radius: 10px;
  transition: width 0.3s ease;
}

.score-fill.excellent {
  background: #28a745;
}
.score-fill.good {
  background: #17a2b8;
}
.score-fill.fair {
  background: #ffc107;
}
.score-fill.poor {
  background: #fd7e14;
}
.score-fill.very-poor {
  background: #dc3545;
}

.score-value {
  font-weight: bold;
  color: #333;
  min-width: 40px;
  text-align: right;
}

.weights-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 0.5rem;
}

.weight-item {
  display: flex;
  justify-content: space-between;
  padding: 0.5rem;
  background: #f8f9fa;
  border-radius: 4px;
}

.weight-label {
  color: #555;
}

.weight-value {
  font-weight: bold;
  color: #333;
}

.no-results {
  text-align: center;
  padding: 3rem;
  color: #666;
  background: #f8f9fa;
  border-radius: 8px;
}

.comparison-controls {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.comparison-controls select {
  flex: 1;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  background: white;
}

.comparison-grid {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr;
  gap: 0.5rem;
}

.comparison-header {
  display: contents;
  font-weight: bold;
  color: #555;
}

.comparison-header > div {
  padding: 0.75rem;
  background: #f8f9fa;
  border-bottom: 2px solid #dee2e6;
}

.comparison-row {
  display: contents;
}

.comparison-row > div {
  padding: 0.75rem;
  border-bottom: 1px solid #dee2e6;
}

.factor-value {
  text-align: center;
  font-weight: 500;
}

@media (max-width: 768px) {
  .form-grid {
    grid-template-columns: 1fr;
  }

  .weight-group {
    grid-template-columns: 1fr;
    gap: 0.25rem;
  }

  .breakdown-item {
    grid-template-columns: 1fr;
    gap: 0.5rem;
  }

  .comparison-controls {
    flex-direction: column;
  }
}
</style>
