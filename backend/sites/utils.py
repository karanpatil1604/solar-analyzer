class SuitabilityCalculator:
    
    def calculate_solar_score(self, solar_irradiance_kwh):
        if solar_irradiance_kwh >= 5.5:
            return 100.0
        elif solar_irradiance_kwh < 3.0:
            return 0.0
        else:
            return ((solar_irradiance_kwh - 3.0) / 2.5) * 100

    def calculate_area_score(self, area_sqm):
        if area_sqm >= 50000:
            return 100.0
        elif area_sqm < 5000:
            return 0.0
        else:
            return ((area_sqm - 5000) / 45000) * 100

    def calculate_grid_score(self, grid_distance_km):
        if grid_distance_km <= 1:
            return 100.0
        elif grid_distance_km >= 20:
            return 0.0
        else:
            return 100 - ((grid_distance_km - 1) / 19) * 100

    def calculate_slope_score(self, slope_degrees):
        if slope_degrees <= 5:
            return 100.0
        elif slope_degrees > 20:
            return 0.0
        elif slope_degrees <= 15:
            return 100 - ((slope_degrees - 5) / 10) * 50
        else:
            return 50 - ((slope_degrees - 15) / 5) * 50

    def calculate_infrastructure_score(self, road_distance_km):
        if road_distance_km <= 0.5:
            return 100.0
        elif road_distance_km >= 5:
            return 0.0
        else:
            return 100 - ((road_distance_km - 0.5) / 4.5) * 100

    def calculate(self, site_data, weights=None):
        if weights is None:
            weights = {
                'solar': 0.35,
                'area': 0.25,
                'grid': 0.20,
                'slope': 0.15,
                'infrastructure': 0.05
            }
        
        scores = {
            'solar': self.calculate_solar_score(site_data['solar_irradiance_kwh']),
            'area': self.calculate_area_score(site_data['area_sqm']),
            'grid': self.calculate_grid_score(site_data['grid_distance_km']),
            'slope': self.calculate_slope_score(site_data['slope_degrees']),
            'infrastructure': self.calculate_infrastructure_score(site_data['road_distance_km'])
        }
        
        total = sum(
            scores[key] * weights[key] 
            for key in scores.keys()
        )
        
        return round(total, 2), scores