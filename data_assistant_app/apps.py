"""
Data Assistant App - Application Configuration

Django application configuration for the Synapse data analysis platform.
"""

from django.apps import AppConfig


class DataAssistantAppConfig(AppConfig):
    """Configuration class for the Data Assistant application."""
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'data_assistant_app'
    verbose_name = 'Data Analysis Assistant'
