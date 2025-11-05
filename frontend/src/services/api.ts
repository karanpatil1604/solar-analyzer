import axios from 'axios'
import type {
  Site,
  AnalysisResult,
  AnalysisParameter,
  SiteFilters,
  Statistics,
  SuitabilityWeights,
} from '../types/index'

const API_BASE_URL = 'http://localhost:8000/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const apiService = {
  // Sites
  async getSites(filters: SiteFilters = {}) {
    const response = await api.get('/sites/', { params: filters })
    return response.data
  },

  async getSite(id: number) {
    const response = await api.get(`/sites/${id}/`)
    return response.data
  },

  // Analysis Results
  async getAnalysisResults(filters: SiteFilters = {}) {
    const response = await api.get('/analysis-results/', { params: filters })
    return response.data
  },

  async getTopSites(limit: number = 10) {
    const response = await api.get('/analysis-results/top_sites/', {
      params: { limit },
    })
    return response.data
  },

  async getStatistics(): Promise<Statistics> {
    const response = await api.get('/analysis-results/statistics/')
    return response.data
  },

  // Analysis Parameters
  async getAnalysisParameters() {
    const response = await api.get('/analysis-parameters/')
    return response.data
  },

  async updateAnalysisParameter(paramId: number, data: Partial<AnalysisParameter>) {
    const response = await api.patch(`/analysis-parameters/${paramId}/`, data)
    return response.data
  },

  // Suitability Analysis
  async calculateSuitability(data: any) {
    const response = await api.post('/analyze/calculate/', data)
    return response.data
  },

  // Export
  async exportSites(format: 'csv' | 'json' = 'csv') {
    const response = await api.get('/export/', {
      params: { format },
      responseType: 'blob',
    })
    return response.data
  },
}

export default api
