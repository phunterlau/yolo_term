#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main entry point for Yolo Terminal game server.
"""

from server import create_app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5001)
