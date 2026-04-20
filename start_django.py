#!/usr/bin/env python
"""
Django development server startup script.
This script starts the Django application on port 8000.
"""
import os
import sys
import django
from django.core.management import execute_from_command_line

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'resumeai_django.settings')
    django.setup()
    
    # Start the development server
    execute_from_command_line(['manage.py', 'runserver', '0.0.0.0:8000'])