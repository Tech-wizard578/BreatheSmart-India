# ==================== Setup Script ====================
# Save as: scripts/setup.sh

#!/bin/bash

# AirSense India Setup Script

set -e

echo "======================================"
echo "AirSense India Setup"
echo "======================================"

# Create necessary directories
echo "Creating directories..."
mkdir -p backend/models
mkdir -p backend/logs
mkdir -p database
mkdir -p scripts
mkdir -p backups
mkdir -p nginx/ssl

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "✓ .env file created. Please edit with your configuration."
else
    echo "✓ .env file already exists"
fi

# Install Python dependencies
echo "Installing Python dependencies..."
cd backend
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cd ..

# Train ML models
echo "Training ML models..."
cd ml
python train_model.py
cd ..

# Initialize database
echo "Initializing database..."
python scripts/manage_db.py init
python scripts/manage_db.py seed

echo ""
echo "======================================"
echo "Setup completed successfully!"
echo "======================================"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your API keys"
echo "2. Run: docker-compose up -d"
echo "3. Access API at: http://localhost:8000/docs"
echo ""