from rest_framework import serializers
from .models import Site, AnalysisResult, AnalysisParameter

class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = '__all__'

class AnalysisResultSerializer(serializers.ModelSerializer):
    site_name = serializers.CharField(source='site.site_name', read_only=True)
    latitude = serializers.DecimalField(source='site.latitude', max_digits=10, decimal_places=7, read_only=True)
    longitude = serializers.DecimalField(source='site.longitude', max_digits=10, decimal_places=7, read_only=True)
    region = serializers.CharField(source='site.region', read_only=True)

    class Meta:
        model = AnalysisResult
        fields = '__all__'

class AnalysisParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalysisParameter
        fields = '__all__'

class SuitabilityCalculatorSerializer(serializers.Serializer):
    solar_irradiance_kwh = serializers.DecimalField(max_digits=4, decimal_places=2)
    area_sqm = serializers.IntegerField()
    grid_distance_km = serializers.DecimalField(max_digits=5, decimal_places=2)
    slope_degrees = serializers.DecimalField(max_digits=4, decimal_places=2)
    road_distance_km = serializers.DecimalField(max_digits=5, decimal_places=2)
    
    solar_weight = serializers.DecimalField(max_digits=4, decimal_places=3, default=0.35)
    area_weight = serializers.DecimalField(max_digits=4, decimal_places=3, default=0.25)
    grid_weight = serializers.DecimalField(max_digits=4, decimal_places=3, default=0.20)
    slope_weight = serializers.DecimalField(max_digits=4, decimal_places=3, default=0.15)
    infra_weight = serializers.DecimalField(max_digits=4, decimal_places=3, default=0.05)