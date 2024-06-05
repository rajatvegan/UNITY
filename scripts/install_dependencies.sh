#!/bin/bash

# Update package lists
sudo apt-get update -y

# Install Python and pip if not already installed
sudo apt-get install -y python3 python3-pip

mkdir UNITY

# Navigate to the application directory
cd /home/ubuntu/UNITY

# Install Python dependencies
pip3 install -r requirements.txt

