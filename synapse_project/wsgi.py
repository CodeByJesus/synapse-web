"""
Synapse Data Platform - WSGI Configuration

WSGI application entry point for production deployment.
"""

import os
from django.core.wsgi import get_wsgi_application

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'synapse_project.settings')

# WSGI application instance
application = get_wsgi_application()
