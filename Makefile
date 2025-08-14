# Grid Optimization System - Makefile

.PHONY: help install install-dev clean test lint format type-check run docker-build docker-run

# Default target
help:
	@echo "Grid Optimization System - Available commands:"
	@echo "  install      Install production dependencies"
	@echo "  install-dev  Install development dependencies"
	@echo "  clean        Clean build artifacts and cache"
	@echo "  test         Run test suite"
	@echo "  lint         Run code linting"
	@echo "  format       Format code with black and isort"
	@echo "  type-check   Run type checking with mypy"
	@echo "  run          Start development server"
	@echo "  docker-build Build Docker image"
	@echo "  docker-run   Run with Docker Compose"

# Installation
install:
	uv pip install -e .

install-dev:
	uv pip install -e ".[dev,docs]"

# Cleaning
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +

# Testing
test:
	pytest tests/ -v --cov=src --cov-report=term-missing

test-fast:
	pytest tests/ -x -v

# Code quality
lint:
	flake8 src tests
	black --check src tests
	isort --check-only src tests

format:
	black src tests
	isort src tests

type-check:
	mypy src

# Development server
run:
	python src/server.py

run-dev:
	uvicorn src.server:app --reload --host 0.0.0.0 --port 8000

# Database
init-db:
	python -c "from src.grid_core.db import init_db; init_db()"

# Docker
docker-build:
	docker build -f deployment/Dockerfile -t grid-optimization .

docker-run:
	docker-compose -f deployment/docker-compose.yml up --build

docker-stop:
	docker-compose -f deployment/docker-compose.yml down

# Unified NAT workflows
run-basic-agent:
	aiq run --config_file configs/workflow.yml --input "Show grid status"

run-reasoning-agent:
	aiq run --config_file configs/workflow-reasoning.yml --input "Analyze grid performance"

run-unified-agent:
	aiq run --config_file src/nat_toolkit/configs/unified-config.yml --input "Comprehensive grid analysis"

# Legacy compatibility tests
test-legacy-functions:
	aiq run --config_file configs/workflow.yml --input "Test legacy optimize_grid function"

# Documentation
docs:
	cd docs && make html

docs-serve:
	cd docs/_build/html && python -m http.server 8080

# Release
build:
	python -m build

upload-test:
	python -m twine upload --repository testpypi dist/*

upload:
	python -m twine upload dist/*