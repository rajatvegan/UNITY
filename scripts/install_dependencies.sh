#!/bin/bash

# Update package lists
sudo apt-get update -y

# Navigate to the application directory
cd /home/ubuntu/UNITY

sudo apt install -y python3-pip
# Install Python dependencies
pip3 install -r requirements.txt

