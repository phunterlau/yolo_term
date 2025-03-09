#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flask application setup for Yolo Terminal game.
"""

from flask import Flask
from flask_cors import CORS

from .routes import api, main

def create_app():
    """
    Create and configure the Flask application.
    
    Returns:
        Flask: Configured Flask application
    """
    # Create Flask app
    app = Flask(__name__, 
                static_folder='../static', 
                template_folder='../templates')
    
    # Enable CORS for all routes
    CORS(app)
    
    # Register blueprints
    app.register_blueprint(main)
    app.register_blueprint(api, url_prefix='/api')
    
    return app
