#!/bin/bash

# Validate that the Flask application is running
curl -f http://localhost:5000 || exit 1
