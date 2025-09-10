#!/bin/bash

# Activate virtual environment and run main.py
.venv/bin/python src/main.py

# Start web server in public directory
cd public && python3 -m http.server 8888
