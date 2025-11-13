"""
WSGI config for Vercel deployment
"""
import os
import sys

# Add project directory to path
sys.path.append(os.path.dirname(__file__))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'searchuniversity.settings')

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

# Vercel serverless function handler
app = application

