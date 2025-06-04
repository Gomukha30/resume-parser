#!/bin/bash

# Exit on error
set -e

echo "Building the production Docker image..."
docker-compose -f docker-compose.prod.yml build

echo "Starting the production container..."
docker-compose -f docker-compose.prod.yml up -d

echo "Container is running!"
echo "Frontend is available at: http://localhost:8000"
echo "API is available at: http://localhost:8000/api"

echo "Tailing the logs (Ctrl+C to exit)..."
docker-compose -f docker-compose.prod.yml logs -f
