#!/bin/bash
echo "Rebuilding the Docker image..."
docker build -t pressing .
docker stop pressing
docker remove pressing
echo "Running the Docker container..."
docker run -d --name pressing -p 8000:8000 pressing
