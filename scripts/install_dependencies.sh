#!/bin/bash

# Update package lists
sudo apt-get update -y

# Navigate to the application directory
cd /home/ubuntu/UNITY

# Install Python dependencies
pip3 install -r requirements.txt

