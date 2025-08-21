"""
Data Assistant App - URL Configuration

Application-specific URL routing for data analysis features.
"""

from django.urls import path
from . import views

# Application URL patterns
urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # API endpoints
    path('api/upload/', views.api_upload_file, name='api_upload'),
    path('api/analysis/<str:filename>/', views.api_get_analysis, name='api_analysis'),
    path('api/clean/<str:filename>/', views.api_clean_data, name='api_clean'),
]