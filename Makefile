# ==================== Makefile ====================
# Save as: Makefile

.PHONY: help install test run docker-up docker-down backup clean

help:
	@echo "AirSense India - Available Commands"
	@echo "===================================="
	@echo "install       - Install dependencies"
	@echo "test          - Run tests"
	@echo "run           - Run development server"
	@echo "docker-up     - Start Docker containers"
	@echo "docker-down   - Stop Docker containers"
	@echo "backup        - Create database backup"
	@echo "clean         - Clean temporary files"

install:
	pip install -r backend/requirements.txt
	python scripts/manage_db.py init
	python scripts/manage_db.py seed

test:
	pytest backend/test_api.py -v

run:
	cd backend && uvicorn main_enhanced:app --reload

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

backup:
	python scripts/manage_db.py backup

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage