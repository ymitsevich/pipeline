# Pipeline Project Makefile
# This Makefile provides common development tasks

.PHONY: help install install-dev test test-cov lint format type-check security audit clean docker-build docker-up docker-down setup-dev

# Default target
help: ## Show this help message
	@echo "Pipeline Project - Available commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Installation and Setup
install: ## Install production dependencies
	pip install -r requirements.txt

install-dev: ## Install all dependencies including dev tools
	pip install -r requirements-dev.txt

setup-dev: install-dev ## Set up development environment
	pre-commit install
	@echo "Development environment setup complete!"

# Code Quality
lint: ## Run all linting tools
	black --check .
	isort --check-only .
	flake8 .

format: ## Format code with black and isort
	black .
	isort .

type-check: ## Run type checking with mypy
	mypy src/

security: ## Run security checks
	bandit -r src/
	safety check

audit: lint type-check security ## Run all code quality checks

# Testing
test: ## Run tests
	pytest

test-cov: ## Run tests with coverage
	pytest --cov=src --cov-report=html --cov-report=term-missing

test-integration: ## Run integration tests
	pytest -m integration

test-unit: ## Run unit tests only
	pytest -m unit

# Docker Operations
docker-build: ## Build Docker image
	docker build -t pipeline:latest .

docker-build-dev: ## Build Docker image for development
	docker build --target development -t pipeline:dev .

docker-up: ## Start all services with docker-compose
	docker-compose up -d

docker-up-build: ## Build and start all services
	docker-compose up -d --build

docker-down: ## Stop all services
	docker-compose down

docker-logs: ## View logs from all services
	docker-compose logs -f

docker-shell: ## Open shell in the main container
	docker-compose exec pipeline bash

# Database Operations
db-up: ## Start only database services
	docker-compose up -d postgres redis

db-init: ## Create database tables from SQLAlchemy models
	DB_HOST=localhost DB_PORT=15432 python scripts/setup_db.py init

db-drop: ## Drop all database tables (prompts for confirmation)
	DB_HOST=localhost DB_PORT=15432 python scripts/setup_db.py drop

db-reset-tables: ## Drop and recreate all tables (prompts for confirmation)
	DB_HOST=localhost DB_PORT=15432 python scripts/setup_db.py reset

db-migrate: ## Run database migrations
	alembic upgrade head

db-downgrade: ## Downgrade database by one revision
	alembic downgrade -1

db-reset: ## Reset database (WARNING: destroys all data)
	docker-compose down -v
	docker-compose up -d postgres
	sleep 10
	$(MAKE) db-migrate

# SQLAlchemy Learning
learn-sqlalchemy: ## Run SQLAlchemy learning script
	DB_HOST=localhost DB_PORT=15432 python scripts/learn_sqlalchemy.py

learn-setup: db-up ## Complete SQLAlchemy learning setup (start DB + create tables)
	@echo "Waiting for Postgres to be ready..."
	@sleep 5
	@$(MAKE) db-init
	@echo ""
	@echo "✅ Database is ready!"
	@echo "Run 'make learn-sqlalchemy' to start the tutorial"

# Development Services
jupyter: ## Start Jupyter Lab
	docker-compose --profile jupyter up -d jupyter
	@echo "Jupyter Lab available at http://localhost:8888 (token: pipeline)"

monitoring: ## Start monitoring stack (Prometheus + Grafana)
	docker-compose --profile monitoring up -d prometheus grafana
	@echo "Prometheus available at http://localhost:9090"
	@echo "Grafana available at http://localhost:3000 (admin:admin)"

# Pipeline Operations
run: ## Run the pipeline locally
	python -m pipeline.cli run

run-docker: ## Run the pipeline in Docker
	docker-compose up pipeline

dry-run: ## Perform a dry run of the pipeline
	python -m pipeline.cli run --dry-run

config: ## Show current configuration
	python -m pipeline.cli config

health: ## Check application health
	python -m pipeline.cli health

# Utility
clean: ## Clean up temporary files and caches
	find . -type d -name "__pycache__" -delete
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	rm -rf build/
	rm -rf dist/
	rm -rf htmlcov/
	rm -rf .coverage

reset: clean ## Reset environment (clean + remove containers + volumes)
	docker-compose down -v --remove-orphans
	docker system prune -f

# CI/CD Simulation
ci-test: ## Simulate CI testing pipeline
	$(MAKE) audit
	$(MAKE) test-cov
	$(MAKE) docker-build

# Development Workflow
dev-setup: setup-dev db-up ## Complete development setup
	@echo "Development environment ready!"
	@echo "Run 'make run' to start the pipeline"
	@echo "Run 'make jupyter' to start Jupyter Lab"
	@echo "Run 'make monitoring' to start monitoring"

# Version and Release (requires poetry-dynamic-versioning or similar)
version: ## Show current version
	poetry version

bump-patch: ## Bump patch version
	poetry version patch

bump-minor: ## Bump minor version
	poetry version minor

bump-major: ## Bump major version
	poetry version major

# Environment Variables
show-env: ## Show environment variables (excluding secrets)
	@echo "Environment Configuration:"
	@echo "========================"
	@env | grep -E "^(PIPELINE_|DB_|LOG_|API_)" | sed 's/=.*PASSWORD.*/=***/' | sort

# Generate requirements lockfiles
requirements: ## Freeze dependencies into requirements files
	pip freeze > requirements.txt
	pip freeze > requirements-dev.txt
