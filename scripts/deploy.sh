# ==================== Deployment Script ====================
# Save as: scripts/deploy.sh

#!/bin/bash

# AirSense India Deployment Script

set -e

echo "======================================"
echo "AirSense India Deployment"
echo "======================================"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

# Check if .env file exists
if [ ! -f .env ]; then
    print_error ".env file not found!"
    echo "Creating from .env.example..."
    cp .env.example .env
    print_warning "Please edit .env file with your configuration"
    exit 1
fi

# Load environment variables
source .env

# Check Docker installation
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed"
    exit 1
fi
print_status "Docker is installed"

# Check Docker Compose
if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose is not installed"
    exit 1
fi
print_status "Docker Compose is installed"

# Pull latest changes (if using Git)
if [ -d .git ]; then
    print_status "Pulling latest changes..."
    git pull
fi

# Build Docker images
print_status "Building Docker images..."
docker-compose build

# Stop existing containers
print_status "Stopping existing containers..."
docker-compose down

# Start services
print_status "Starting services..."
docker-compose up -d

# Wait for services to be ready
print_status "Waiting for services to be ready..."
sleep 10

# Check if backend is healthy
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    print_status "Backend is healthy"
else
    print_error "Backend health check failed"
    docker-compose logs backend
    exit 1
fi

# Run database migrations (if needed)
print_status "Running database migrations..."
docker-compose exec backend python scripts/manage_db.py init

# Show running containers
print_status "Running containers:"
docker-compose ps

# Show logs
print_warning "Showing recent logs..."
docker-compose logs --tail=50

echo ""
print_status "Deployment completed successfully!"
echo ""
echo "Access the application at:"
echo "  - API: http://localhost:8000"
echo "  - Docs: http://localhost:8000/docs"
echo ""
echo "To view logs: docker-compose logs -f"
echo "To stop: docker-compose down"
echo ""