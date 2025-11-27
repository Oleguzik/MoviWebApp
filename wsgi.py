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
# Note: 'application' is used by the WSGI server, not within this file
from app import app as application  # noqa: F401

# PythonAnywhere expects the variable to be named 'application'
