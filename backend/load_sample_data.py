import os
import django
import pandas as pd

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "solar_analyzer.settings")  
django.setup()

from sites.models import Site, AnalysisResult
from sites.utils import SuitabilityCalculator

CSV_PATH = "solar_sites_data.csv"  # ✅ Update path if stored elsewhere

def load_from_csv():
    print("Loading sites from CSV:", CSV_PATH)

    # Load CSV values as DataFrame
    df = pd.read_csv(CSV_PATH)

    # Optional → clear old records
    # Site.objects.all().delete()
    # AnalysisResult.objects.all().delete()

    # Default weights
    weights = {
        'solar': 0.35,
        'area': 0.25,
        'grid': 0.20,
        'slope': 0.15,
        'infrastructure': 0.05
    }

    calculator = SuitabilityCalculator()

    for _, row in df.iterrows():
        site_data = {
            'site_name': row['site_name'],
            'latitude': row['latitude'],
            'longitude': row['longitude'],
            'area_sqm': row['area_sqm'],
            'solar_irradiance_kwh': row['solar_irradiance_kwh'],
            'grid_distance_km': row['grid_distance_km'],
            'slope_degrees': row['slope_degrees'],
            'road_distance_km': row['road_distance_km'],
            'elevation_m': row['elevation_m'],
            'land_type': row['land_type'],
            'region': row['region']
        }

        site = Site.objects.create(**site_data)

        total_score, breakdown = calculator.calculate(site_data, weights)

        AnalysisResult.objects.create(
            site=site,
            solar_irradiance_score=breakdown['solar'],
            area_score=breakdown['area'],
            grid_distance_score=breakdown['grid'],
            slope_score=breakdown['slope'],
            infrastructure_score=breakdown['infrastructure'],
            total_suitability_score=total_score,
            parameters_snapshot=weights
        )

    print(f"Successfully imported {len(df)} sites and generated analysis results!")

if __name__ == "__main__":
    load_from_csv()
