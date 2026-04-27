#!/bin/bash
# Simple test script to validate the pipeline

echo "Testing Multi-Agent Digest Pipeline"
echo "===================================="

# Check if Docker is running
docker --version > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "ERROR: Docker is not installed or running"
    exit 1
fi

# Set required environment variable (or skip if you want to use defaults)
export GEMINI_API_KEY=${GEMINI_API_KEY:-"test-key-for-development"}

# Build and run services
echo "Building Docker images..."
docker-compose build

echo ""
echo "Running pipeline..."
docker-compose up

echo ""
echo "Pipeline completed!"
echo "Check ./multi-agents-digest/output/daily_digest.md for results"
