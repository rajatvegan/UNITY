# Use an official Python runtime as a parent image
FROM python:3.12
# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose port 80 for the nginx server
# EXPOSE 80

# Install nginx
RUN apt-get update && apt-get install -y nginx

# Copy the nginx configuration file into the container
COPY nginx.conf /etc/nginx/nginx.conf

# Start the nginx server and the Flask app
CMD service nginx start && python wsgi.py
