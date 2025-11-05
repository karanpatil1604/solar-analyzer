from rest_framework import serializers
from .models import Site, AnalysisResult, AnalysisParameter
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation

class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = '__all__'

class AnalysisResultSerializer(serializers.ModelSerializer):
    site_name = serializers.CharField(source='site.site_name', read_only=True)
    latitude = serializers.DecimalField(source='site.latitude', max_digits=10, decimal_places=7, read_only=True)
    longitude = serializers.DecimalField(source='site.longitude', max_digits=10, decimal_places=7, read_only=True)
    region = serializers.CharField(source='site.region', read_only=True)
    area_sqm = serializers.IntegerField(source='site.area_sqm', read_only=True)
    land_type = serializers.CharField(source='site.land_type', read_only=True)
    solar_irradiance_kwh = serializers.FloatField(source='site.solar_irradiance_kwh', read_only=True)
    class Meta:
        model = AnalysisResult
        fields = '__all__'

class AnalysisParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalysisParameter
        fields = '__all__'

class SuitabilityCalculatorSerializer(serializers.Serializer):
    solar_irradiance_kwh = serializers.DecimalField(max_digits=10, decimal_places=2)
    area_sqm = serializers.IntegerField()
    grid_distance_km = serializers.DecimalField(max_digits=10, decimal_places=4)
    slope_degrees = serializers.DecimalField(max_digits=10, decimal_places=4)
    road_distance_km = serializers.DecimalField(max_digits=10, decimal_places=4)

    solar_weight = serializers.DecimalField(max_digits=30, decimal_places=30, default=0.35)
    area_weight = serializers.DecimalField(max_digits=30, decimal_places=30, default=0.25)
    grid_weight = serializers.DecimalField(max_digits=30, decimal_places=30, default=0.20)
    slope_weight = serializers.DecimalField(max_digits=30, decimal_places=30, default=0.15)
    infra_weight = serializers.DecimalField(max_digits=30, decimal_places=30, default=0.05)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        ks = [ 'solar_weight','area_weight','grid_weight','slope_weight','infra_weight']
        for key, value in data.items():
            if value is None or key not in ks:
                continue

            try:
                value = Decimal(str(value))
                data[key] = str(value.quantize(Decimal("0.00"), rounding=ROUND_HALF_UP))
            except (InvalidOperation, ValueError):
                continue

        return data