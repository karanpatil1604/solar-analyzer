export interface Site {
  site_id: number
  site_name: string
  latitude: number
  longitude: number
  area_sqm: number
  solar_irradiance_kwh: number
  grid_distance_km: number
  slope_degrees: number
  road_distance_km: number
  elevation_m: number
  land_type: string
  region: string
  created_at: string
  updated_at: string
}

export interface AnalysisResult {
  result_id: number
  site: number
  site_name: string
  latitude: number
  longitude: number
  region: string
  solar_irradiance_score: number
  area_score: number
  grid_distance_score: number
  slope_score: number
  infrastructure_score: number
  total_suitability_score: number
  analysis_timestamp: string
  parameters_snapshot: any
}

export interface AnalysisParameter {
  param_id: number
  parameter_name: string
  weight_value: number
  description: string
  is_active: boolean
}

export interface SuitabilityWeights {
  solar_weight: number
  area_weight: number
  grid_weight: number
  slope_weight: number
  infra_weight: number
}

export interface SiteFilters {
  min_score?: number
  max_score?: number
  region?: string
  land_type?: string
  limit?: number
  site_id?: number
}

export interface Statistics {
  total_sites: number
  avg_score: number
  min_score: number
  max_score: number
}
