from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Site(models.Model):
    site_id = models.AutoField(primary_key=True)
    site_name = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=10, decimal_places=7)
    longitude = models.DecimalField(max_digits=10, decimal_places=7)
    area_sqm = models.IntegerField()
    solar_irradiance_kwh = models.DecimalField(max_digits=4, decimal_places=2)
    grid_distance_km = models.DecimalField(max_digits=5, decimal_places=2)
    slope_degrees = models.DecimalField(max_digits=4, decimal_places=2)
    road_distance_km = models.DecimalField(max_digits=5, decimal_places=2)
    elevation_m = models.IntegerField()
    land_type = models.CharField(max_length=50)
    region = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'sites'
        indexes = [
            models.Index(fields=['latitude']),
            models.Index(fields=['longitude']),
            models.Index(fields=['region']),
            models.Index(fields=['land_type']),
        ]
    
    def calculate_suitability_scores(self, weights=None):
        """Calculate suitability scores for this site"""
        from .utils import SuitabilityCalculator
        
        if weights is None:
            # Get default weights from parameters
            try:
                from .models import AnalysisParameter
                weights = {
                    'solar': float(AnalysisParameter.objects.get(parameter_name='solar_irradiance_weight').weight_value),
                    'area': float(AnalysisParameter.objects.get(parameter_name='area_weight').weight_value),
                    'grid': float(AnalysisParameter.objects.get(parameter_name='grid_distance_weight').weight_value),
                    'slope': float(AnalysisParameter.objects.get(parameter_name='slope_weight').weight_value),
                    'infrastructure': float(AnalysisParameter.objects.get(parameter_name='infrastructure_weight').weight_value),
                }
            except AnalysisParameter.DoesNotExist:
                weights = {
                    'solar': 0.35,
                    'area': 0.25,
                    'grid': 0.20,
                    'slope': 0.15,
                    'infrastructure': 0.05
                }
        
        calculator = SuitabilityCalculator()
        site_data = {
            'solar_irradiance_kwh': float(self.solar_irradiance_kwh),
            'area_sqm': self.area_sqm,
            'grid_distance_km': float(self.grid_distance_km),
            'slope_degrees': float(self.slope_degrees),
            'road_distance_km': float(self.road_distance_km)
        }
        
        total_score, breakdown = calculator.calculate(site_data, weights)
        
        # Create or update analysis result
        analysis_result, created = AnalysisResult.objects.update_or_create(
            site=self,
            defaults={
                'solar_irradiance_score': breakdown['solar'],
                'area_score': breakdown['area'],
                'grid_distance_score': breakdown['grid'],
                'slope_score': breakdown['slope'],
                'infrastructure_score': breakdown['infrastructure'],
                'total_suitability_score': total_score,
                'parameters_snapshot': weights
            }
        )
        
        return analysis_result
    def get_latest_score(self):
        """Get the latest analysis result for this site"""
        try:
            return AnalysisResult.objects.filter(site=self).latest('analysis_timestamp')
        except AnalysisResult.DoesNotExist:
            return None
class AnalysisParameter(models.Model):
    param_id = models.AutoField(primary_key=True)
    parameter_name = models.CharField(max_length=100, unique=True)
    weight_value = models.DecimalField(
        max_digits=4, 
        decimal_places=3,
        validators=[MinValueValidator(0), MaxValueValidator(1)]
    )
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'analysis_parameters'

class AnalysisResult(models.Model):
    result_id = models.AutoField(primary_key=True)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    solar_irradiance_score = models.DecimalField(max_digits=5, decimal_places=2)
    area_score = models.DecimalField(max_digits=5, decimal_places=2)
    grid_distance_score = models.DecimalField(max_digits=5, decimal_places=2)
    slope_score = models.DecimalField(max_digits=5, decimal_places=2)
    infrastructure_score = models.DecimalField(max_digits=5, decimal_places=2)
    total_suitability_score = models.DecimalField(max_digits=5, decimal_places=2)
    analysis_timestamp = models.DateTimeField(auto_now_add=True)
    parameters_snapshot = models.JSONField(blank=True, null=True)

    class Meta:
        db_table = 'analysis_results'
        indexes = [
            models.Index(fields=['total_suitability_score']),
            models.Index(fields=['site']),
            models.Index(fields=['analysis_timestamp']),
        ]
    
    def get_score_breakdown(self):
        """Return score breakdown as dictionary"""
        return {
            'solar_irradiance': float(self.solar_irradiance_score),
            'area': float(self.area_score),
            'grid_distance': float(self.grid_distance_score),
            'slope': float(self.slope_score),
            'infrastructure': float(self.infrastructure_score),
            'total': float(self.total_suitability_score)
        }