"""
Synapse Data Platform - ASGI Configuration

ASGI application entry point for async deployment.
"""

import os
from django.core.asgi import get_asgi_application

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'synapse_project.settings')

# ASGI application instance
application = get_asgi_application()
