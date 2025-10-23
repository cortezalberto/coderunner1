#!/bin/bash
set -e

echo "🐍 Python Playground Suite - Starting..."
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Error: Docker is not running"
    echo "Please start Docker and try again"
    exit 1
fi

echo "✅ Docker is running"
echo ""

# Build runner image
echo "📦 Building sandbox runner image..."
docker build -t py-playground-runner:latest ./runner
echo "✅ Runner image built"
echo ""

# Start services
echo "🚀 Starting all services with Docker Compose..."
docker compose up --build

# Note: docker compose up --build will start:
# - PostgreSQL (port 5432)
# - Redis (port 6379)
# - Backend API (port 8000)
# - Worker (background)
# - Frontend (port 5173)
