# WSGI entry point for PythonAnywhere deployment
# This file tells PythonAnywhere how to run your Flask app

import sys
import os

# Add your project directory to the sys.path
# Replace 'yourusername' with your actual PythonAnywhere username
project_home = '/home/yourusername/MoviWebApp'
if project_home not in sys.path:
	sys.path.insert(0, project_home)

# Set environment variables (if not using .env file on server)
os.environ['FLASK_ENV'] = 'production'

# Import your Flask app
from app import app as application

# Note: PythonAnywhere expects the variable to be named 'application'
