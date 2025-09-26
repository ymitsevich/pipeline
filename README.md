# Pipeline - Modern Python Data Engineering Application

[![CI/CD Pipeline](https://github.com/username/pipeline/workflows/CI/CD%20Pipeline/badge.svg)](https://github.com/username/pipeline/actions)
[![codecov](https://codecov.io/gh/username/pipeline/branch/main/graph/badge.svg)](https://codecov.io/gh/username/pipeline)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A modern, production-ready Python application skeleton that follows data engineering and software development best practices. Built with Poetry, Docker, comprehensive testing, and CI/CD workflows.

## ✨ Features

- **🏗️ Modern Python Project Structure** - Clean, scalable architecture
- **📦 Poetry Package Management** - Dependency management and virtual environments  
- **🐳 Docker & Docker Compose** - Containerized development and deployment
- **⚡ FastAPI Ready** - API framework integration preparation
- **🗄️ Database Integration** - PostgreSQL with SQLAlchemy and Alembic
- **📊 Structured Logging** - JSON logging with correlation IDs
- **🧪 Comprehensive Testing** - Unit, integration, and performance tests
- **🔍 Code Quality Tools** - Black, isort, flake8, mypy, bandit
- **🔄 CI/CD Workflows** - GitHub Actions with automated testing and deployment
- **📈 Monitoring Ready** - Prometheus, Grafana, and health checks
- **🛠️ Development Tools** - Makefile, pre-commit hooks, Jupyter Lab

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- [Poetry](https://python-poetry.org/docs/#installation)
- Docker and Docker Compose (optional)

### Installation

1. **Clone and set up the project:**
   ```bash
   git clone <repository-url>
   cd pipeline
   make dev-setup
   ```

2. **Or using Docker:**
   ```bash
   docker-compose up --build
   ```

### Basic Usage

```bash
# Run the pipeline
make run

# Run with Docker
make run-docker

# Check application health
make health

# View configuration
make config
```

## 📖 Documentation

- [Installation Guide](docs/installation.md)
- [Development Setup](docs/development.md)
- [API Documentation](docs/api.md)
- [Deployment Guide](docs/deployment.md)
- [Contributing Guidelines](docs/contributing.md)

## 🏗️ Project Structure

```
pipeline/
├── src/pipeline/           # Main application code
│   ├── core/              # Core business logic
│   ├── data/              # Data processing modules
│   ├── config/            # Configuration management
│   └── utils/             # Utility functions
├── tests/                 # Test suite
│   ├── unit/              # Unit tests
│   └── integration/       # Integration tests
├── docs/                  # Documentation
├── scripts/               # Utility scripts
├── config/                # Configuration files
├── data/                  # Data directories
├── docker-compose.yml     # Docker services
├── Dockerfile             # Container definition
├── Makefile              # Development commands
└── pyproject.toml        # Project configuration
```

## 🛠️ Development

### Common Commands

```bash
# Development environment
make dev-setup              # Complete development setup
make install-dev           # Install all dependencies
make clean                 # Clean temporary files

# Code Quality
make format                # Format code
make lint                  # Run linters
make type-check           # Type checking
make security             # Security checks
make audit                # Run all checks

# Testing
make test                 # Run all tests
make test-unit           # Unit tests only
make test-integration    # Integration tests only
make test-cov            # Tests with coverage

# Docker
make docker-build        # Build Docker image
make docker-up          # Start all services
make docker-down        # Stop all services

# Database
make db-up              # Start database services
make db-migrate         # Run migrations
make db-reset          # Reset database

# Additional Services
make jupyter           # Start Jupyter Lab
make monitoring        # Start monitoring stack
```

### Pre-commit Hooks

The project uses pre-commit hooks to ensure code quality:

```bash
# Install hooks
poetry run pre-commit install

# Run manually
poetry run pre-commit run --all-files
```

## 🐳 Docker Services

The application includes several containerized services:

- **pipeline** - Main application
- **postgres** - PostgreSQL database
- **redis** - Redis cache
- **jupyter** - Jupyter Lab (development profile)
- **prometheus** - Metrics collection (monitoring profile) 
- **grafana** - Monitoring dashboard (monitoring profile)

### Service URLs

- Application: http://localhost:8000
- Jupyter Lab: http://localhost:8888 (token: pipeline)
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (admin:admin)

## ⚙️ Configuration

Configuration is managed through environment variables and Pydantic settings:

```bash
# Copy example environment file
cp .env.example .env

# Edit configuration
vim .env
```

Key configuration areas:
- Application settings (debug, environment)
- Database connection
- Logging configuration
- Processing parameters

## 📊 Monitoring & Observability

The application includes built-in monitoring capabilities:

- **Health Checks** - Application and dependency health endpoints
- **Structured Logging** - JSON logs with correlation IDs
- **Metrics** - Prometheus-compatible metrics (ready for integration)
- **Tracing** - Distributed tracing preparation

## 🧪 Testing

Comprehensive testing setup with different test categories:

```bash
# Run specific test categories
pytest -m unit              # Unit tests only
pytest -m integration       # Integration tests
pytest -m "not slow"        # Skip slow tests

# Coverage reporting
pytest --cov=src --cov-report=html
```

## 🚀 Deployment

### Production Deployment

1. **Build production image:**
   ```bash
   docker build --target production -t pipeline:prod .
   ```

2. **Deploy with docker-compose:**
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

3. **Or use the Makefile:**
   ```bash
   make deploy-production
   ```

## 🤝 Contributing

Please read [CONTRIBUTING.md](docs/contributing.md) for details on our code of conduct and development process.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and quality checks (`make audit`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with modern Python best practices
- Inspired by data engineering and MLOps patterns
- Uses industry-standard tools and frameworks

---

**Note:** This is a project skeleton. Customize it according to your specific requirements and use cases.
