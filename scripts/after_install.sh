#!/bin/bash

# Navigate to the application directory
cd /home/ubuntu/UNITY

# Activate the virtual environment
source venv/bin/activate

# Ensure all dependencies are installed (optional, since they should already be there)
pip install -r requirements.txt
