"""
Data Assistant App - URL Configuration

Application-specific URL routing for data analysis features.
"""

from django.urls import path
from . import views

# Application URL patterns
urlpatterns = [
    path('', views.home, name='home'),
]