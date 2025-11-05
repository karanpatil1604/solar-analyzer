from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'sites', views.SiteViewSet)
router.register(r'analysis-results', views.AnalysisResultViewSet)
router.register(r'analysis-parameters', views.AnalysisParameterViewSet)
router.register(r'analyze', views.SuitabilityAnalysisViewSet, basename='analyze')

urlpatterns = [
    path('api/', include(router.urls)),
]