#!/bin/bash

# Define the image name
IMAGE_NAME="flask-smorest-api"

# Find the container ID using the image name
CONTAINER_ID=$(docker ps -q -f ancestor=$IMAGE_NAME)

if [ ! -z "$CONTAINER_ID" ]; then
    echo "Stopping and removing existing container..."
    docker stop $CONTAINER_ID
    docker rm $CONTAINER_ID
fi

echo "Running a new container..."
docker run -dp 5001:5000 -w /app -v "$(pwd):/app" $IMAGE_NAME