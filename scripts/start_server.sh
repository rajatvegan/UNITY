#!/bin/bash

# Navigate to the application directory
cd /home/ubuntu/UNITY

# Start the Flask application
# Assuming your Flask app entry point is app.py and it listens on port 5000
nohup python3 app.py > app.log 2>&1 &
