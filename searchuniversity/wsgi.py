"""
WSGI config wrapper for Vercel deployment
"""
from searchuniversity.wsgi import application

# Vercel serverless function handler
app = application

