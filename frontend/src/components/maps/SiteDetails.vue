<template>
  <div class="site-details" v-if="site">
    <h3>{{ site.site_name }}</h3>

    <div class="score-section">
      <div class="total-score" :class="getScoreClass(site.total_suitability_score)">
        {{ formatScore(site.total_suitability_score) }}
      </div>
      <div class="score-label">Overall Suitability Score</div>
    </div>

    <div class="details-grid">
      <div class="detail-item">
        <label>Region:</label>
        <span>{{ site.region }}</span>
      </div>
      <!-- <div class="detail-item">
        <label>Land Type:</label>
        <span>{{ site?.land_type }}</span>
      </div>
      <div class="detail-item">
        <label>Area:</label>
        <span>{{ site?.area_sqm?.toLocaleString?.() || 'N/A' }} m²</span>
      </div> -->
      <div class="detail-item">
        <label>Solar Irradiance:</label>
        <span>{{ site.solar_irradiance_score || '0.0' }} kWh/m²/day</span>
      </div>
    </div>

    <div class="breakdown-section">
      <h4>Score Breakdown</h4>
      <div class="breakdown-grid">
        <div class="breakdown-item">
          <div class="breakdown-label">Solar</div>
          <div class="breakdown-bar">
            <div class="breakdown-fill" :style="{ width: site.solar_irradiance_score + '%' }"></div>
          </div>
          <div class="breakdown-value">{{ site?.solar_irradiance_score }}</div>
        </div>
        <div class="breakdown-item">
          <div class="breakdown-label">Area</div>
          <div class="breakdown-bar">
            <div class="breakdown-fill" :style="{ width: site.area_score + '%' }"></div>
          </div>
          <div class="breakdown-value">{{ site.area_score }}</div>
        </div>
        <div class="breakdown-item">
          <div class="breakdown-label">Grid Distance</div>
          <div class="breakdown-bar">
            <div class="breakdown-fill" :style="{ width: site.grid_distance_score + '%' }"></div>
          </div>
          <div class="breakdown-value">{{ site.grid_distance_score }}</div>
        </div>
        <div class="breakdown-item">
          <div class="breakdown-label">Slope</div>
          <div class="breakdown-bar">
            <div class="breakdown-fill" :style="{ width: site.slope_score + '%' }"></div>
          </div>
          <div class="breakdown-value">{{ site.slope_score }}</div>
        </div>
        <div class="breakdown-item">
          <div class="breakdown-label">Infrastructure</div>
          <div class="breakdown-bar">
            <div class="breakdown-fill" :style="{ width: site.infrastructure_score + '%' }"></div>
          </div>
          <div class="breakdown-value">{{ site.infrastructure_score }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { AnalysisResult } from '@/types'

interface Props {
  site: AnalysisResult
}

defineProps<Props>()
const formatScore = (score: any) => {
  return typeof score == 'number' ? Number(score).toFixed(2) : Number(score)
}

const getScoreClass = (score: number) => {
  if (score >= 80) return 'excellent'
  if (score >= 60) return 'good'
  if (score >= 40) return 'fair'
  if (score >= 20) return 'poor'
  return 'very-poor'
}
</script>

<style scoped>
.site-details {
  padding: 10px;
}

h3 {
  margin: 0 0 20px 0;
  color: #333;
}

.score-section {
  text-align: center;
  margin-bottom: 20px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
}

.total-score {
  font-size: 3em;
  font-weight: bold;
  margin-bottom: 5px;
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
  font-size: 0.9em;
}

.details-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
  margin-bottom: 20px;
}

.detail-item {
  display: flex;
  justify-content: between;
}

.detail-item label {
  font-weight: bold;
  color: #555;
  margin-right: 10px;
}

.breakdown-section h4 {
  margin: 0 0 15px 0;
  color: #333;
}

.breakdown-grid {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.breakdown-item {
  display: flex;
  align-items: center;
  gap: 10px;
}

.breakdown-label {
  min-width: 100px;
  font-weight: 500;
  color: #555;
}

.breakdown-bar {
  flex: 1;
  height: 20px;
  background: #e9ecef;
  border-radius: 10px;
  overflow: hidden;
}

.breakdown-fill {
  height: 100%;
  background: linear-gradient(90deg, #dc3545, #fd7e14, #ffc107, #17a2b8, #28a745);
  border-radius: 10px;
  transition: width 0.3s ease;
}

.breakdown-value {
  min-width: 40px;
  text-align: right;
  font-weight: bold;
  color: #333;
}
</style>
