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