from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Site, AnalysisResult, AnalysisParameter
from .serializers import (
    SiteSerializer, 
    AnalysisResultSerializer, 
    AnalysisParameterSerializer,
    SuitabilityCalculatorSerializer
)
from .utils import SuitabilityCalculator

class SiteViewSet(viewsets.ModelViewSet):
    queryset = Site.objects.all()
    serializer_class = SiteSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['region', 'land_type']

class AnalysisResultViewSet(viewsets.ModelViewSet):
    queryset = AnalysisResult.objects.all()
    serializer_class = AnalysisResultSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['site__region', 'site__land_type']

    def get_queryset(self):
        queryset = AnalysisResult.objects.select_related('site').all()
        
        # Filter by score range
        min_score = self.request.query_params.get('min_score')
        max_score = self.request.query_params.get('max_score')
        
        if min_score is not None:
            queryset = queryset.filter(total_suitability_score__gte=min_score)
        if max_score is not None:
            queryset = queryset.filter(total_suitability_score__lte=max_score)
            
        return queryset

    @action(detail=False, methods=['get'])
    def top_sites(self, request):
        limit = int(request.query_params.get('limit', 10))
        queryset = self.get_queryset().order_by('-total_suitability_score')[:limit]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        from django.db.models import Avg, Max, Min, StdDev, Count
        
        stats = AnalysisResult.objects.aggregate(
            total_sites=Count('result_id'),
            avg_score=Avg('total_suitability_score'),
            min_score=Min('total_suitability_score'),
            max_score=Max('total_suitability_score'),
        )
        
        return Response(stats)

class AnalysisParameterViewSet(viewsets.ModelViewSet):
    queryset = AnalysisParameter.objects.all()
    serializer_class = AnalysisParameterSerializer

class SuitabilityAnalysisViewSet(viewsets.ViewSet):
    
    @action(detail=False, methods=['post'])
    def calculate(self, request):
        serializer = SuitabilityCalculatorSerializer(data=request.data)
        if serializer.is_valid():
            calculator = SuitabilityCalculator()
            data = serializer.validated_data
            
            weights = {
                'solar': data.get('solar_weight', 0.35),
                'area': data.get('area_weight', 0.25),
                'grid': data.get('grid_weight', 0.20),
                'slope': data.get('slope_weight', 0.15),
                'infrastructure': data.get('infra_weight', 0.05)
            }
            
            site_data = {
                'solar_irradiance_kwh': data['solar_irradiance_kwh'],
                'area_sqm': data['area_sqm'],
                'grid_distance_km': data['grid_distance_km'],
                'slope_degrees': data['slope_degrees'],
                'road_distance_km': data['road_distance_km']
            }
            
            total_score, breakdown = calculator.calculate(site_data, weights)
            
            return Response({
                'total_score': total_score,
                'breakdown': breakdown,
                'weights_used': weights
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)