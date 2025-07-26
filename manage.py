#!/usr/bin/env python
"""
Synapse Data Platform - Management Script

Django command-line utility for administrative tasks.
"""
import os
import sys


def main():
    """Execute Django management commands."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'synapse_project.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Django not found. Please ensure Django is installed and "
            "your virtual environment is activated."
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
