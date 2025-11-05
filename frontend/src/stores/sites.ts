import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Site, AnalysisResult, SiteFilters, Statistics, SuitabilityWeights } from '@/types'
import { apiService } from '@/services/api'

export const useSitesStore = defineStore('sites', () => {
  // State
  const sites = ref<Site[]>([])
  const analysisResults = ref<AnalysisResult[]>([])
  const currentSite = ref<Site | null>(null)
  const currentAnalysis = ref<AnalysisResult | null>(null)
  const statistics = ref<Statistics | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)
  const filters = ref<SiteFilters>({
    min_score: 0,
    max_score: 100,
    limit: 50,
  })

  // Getters
  const filteredSites = computed(() => {
    return analysisResults.value.filter((result) => {
      const score = result.total_suitability_score
      return score >= (filters.value.min_score || 0) && score <= (filters.value.max_score || 100)
    })
  })

  const topSites = computed(() => {
    return [...analysisResults.value]
      .sort((a, b) => b.total_suitability_score - a.total_suitability_score)
      .slice(0, 10)
  })

  const scoreDistribution = computed(() => {
    const distribution = {
      excellent: 0,
      good: 0,
      fair: 0,
      poor: 0,
      veryPoor: 0,
    }

    analysisResults.value.forEach((result) => {
      const score = result.total_suitability_score
      if (score >= 80) distribution.excellent++
      else if (score >= 60) distribution.good++
      else if (score >= 40) distribution.fair++
      else if (score >= 20) distribution.poor++
      else distribution.veryPoor++
    })

    return distribution
  })

  // Actions
  const fetchSites = async (customFilters?: SiteFilters) => {
    loading.value = true
    error.value = null
    try {
      if (customFilters) {
        filters.value = { ...filters.value, ...customFilters }
      }
      const data = await apiService.getAnalysisResults(filters.value)
      analysisResults.value = data.results || data
    } catch (err: any) {
      error.value = err.message || 'Failed to fetch sites'
    } finally {
      loading.value = false
    }
  }

  const fetchSiteDetails = async (siteId: number) => {
    loading.value = true
    try {
      const [siteData, analysisData] = await Promise.all([
        apiService.getSite(siteId),
        apiService.getAnalysisResults({ site_id: siteId }),
      ])
      currentSite.value = siteData
      currentAnalysis.value = analysisData.results?.[0] || analysisData[0] || null
    } catch (err: any) {
      error.value = err.message || 'Failed to fetch site details'
    } finally {
      loading.value = false
    }
  }

  const fetchStatistics = async () => {
    try {
      statistics.value = await apiService.getStatistics()
    } catch (err: any) {
      error.value = err.message || 'Failed to fetch statistics'
    }
  }

  const fetchTopSites = async (limit: number = 10) => {
    try {
      const data = await apiService.getTopSites(limit)
      analysisResults.value = data.results || data
    } catch (err: any) {
      error.value = err.message || 'Failed to fetch top sites'
    }
  }
  const clamp = (value: any) => {
    let v = parseFloat(value)
    if (isNaN(v)) return 0

    // Limit range
    if (v < 0) v = 0
    if (v > 100) v = 100

    // Max 2 decimals always
    v = Math.round(v * 100) / 100

    // Ensure max 4 characters ignoring decimal
    const digits = v.toString().replace('.', '')
    if (digits.length > 4) {
      v = parseFloat(digits.slice(0, 4 - 2) + '.' + digits.slice(4 - 2, 4))
    }

    return v
  } 
  const calculateCustomSuitability = async (siteData: any, weights: SuitabilityWeights) => {
    try {
      const sanitizedWeights = {
        solar_weight: clamp(weights.solar_weight),
        area_weight: clamp(weights.area_weight),
        grid_weight: clamp(weights.grid_weight),
        slope_weight: clamp(weights.slope_weight),
        infra_weight: clamp(weights.infra_weight),
      }
      console.log('Final weights', sanitizedWeights)

      const data = { ...siteData, ...sanitizedWeights }
      return await apiService.calculateSuitability(data)
    } catch (err: any) {
      error.value = err.message || 'Failed to calculate suitability'
      throw err
    }
  }

  const exportData = async (format: 'csv' | 'json' = 'csv') => {
    try {
      const blob = await apiService.exportSites(format)
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = `solar_sites.${format}`
      link.click()
      window.URL.revokeObjectURL(url)
    } catch (err: any) {
      error.value = err.message || 'Failed to export data'
    }
  }

  const updateFilters = (newFilters: SiteFilters) => {
    filters.value = { ...filters.value, ...newFilters }
    fetchSites()
  }

  const clearError = () => {
    error.value = null
  }

  return {
    // State
    sites,
    analysisResults,
    currentSite,
    currentAnalysis,
    statistics,
    loading,
    error,
    filters,

    // Getters
    filteredSites,
    topSites,
    scoreDistribution,

    // Actions
    fetchSites,
    fetchSiteDetails,
    fetchStatistics,
    fetchTopSites,
    calculateCustomSuitability,
    exportData,
    updateFilters,
    clearError,
  }
})
