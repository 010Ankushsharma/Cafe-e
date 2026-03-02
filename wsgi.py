"""
WSGI entry point for Render deployment.
This file provides a clean entry point for gunicorn.
"""
import os
from app import create_app

# Set production environment
os.environ.setdefault('FLASK_ENV', 'production')

# Create the application instance
application = create_app()

if __name__ == '__main__':
    application.run()
