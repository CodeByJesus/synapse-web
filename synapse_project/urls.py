"""
Synapse Data Platform - URL Configuration

Main URL routing for the Synapse application.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# URL patterns for the main application
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('data_assistant_app.urls')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)