# Development Guide

This guide covers setting up a development environment and contributing to the pipeline project.

## Prerequisites

- Python 3.11 or higher
- [Poetry](https://python-poetry.org/docs/#installation) for dependency management
- Docker and Docker Compose (recommended)
- Git

## Development Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd pipeline
```

### 2. Set Up Development Environment

The easiest way to set up your development environment is using the provided Makefile:

```bash
make dev-setup
```

This command will:
- Install Poetry if not available
- Install all dependencies (including dev and test dependencies)
- Set up pre-commit hooks
- Start database services with Docker

### 3. Manual Setup (Alternative)

If you prefer manual setup:

```bash
# Install dependencies
poetry install --with dev,test

# Set up pre-commit hooks
poetry run pre-commit install

# Start database services
docker-compose up -d postgres redis
```

### 4. Verify Installation

```bash
# Check if everything is working
make health

# Run tests
make test

# Check code quality
make audit
```

## Development Workflow

### Code Style and Quality

The project uses several tools to maintain code quality:

- **Black** - Code formatting
- **isort** - Import sorting
- **flake8** - Linting
- **mypy** - Type checking
- **bandit** - Security analysis

Run all quality checks:
```bash
make audit
```

Or run individual tools:
```bash
make format      # Format code with black and isort
make lint        # Run flake8
make type-check  # Run mypy
make security    # Run bandit and safety
```

### Testing

Write comprehensive tests for your code:

```bash
# Run all tests
make test

# Run specific test categories
make test-unit
make test-integration

# Run with coverage
make test-cov
```

Test structure:
- `tests/unit/` - Unit tests for individual components
- `tests/integration/` - Integration tests for component interaction
- `tests/conftest.py` - Shared fixtures and configuration

### Database Development

Working with the database:

```bash
# Start database services
make db-up

# Create and run migrations
alembic revision --autogenerate -m "Description of changes"
make db-migrate

# Reset database (WARNING: destroys all data)
make db-reset
```

### Docker Development

Use Docker for consistent development environments:

```bash
# Build development image
make docker-build-dev

# Start all services
make docker-up

# View logs
make docker-logs

# Open shell in container
make docker-shell

# Stop all services
make docker-down
```

### Additional Development Tools

#### Jupyter Lab

For data analysis and experimentation:

```bash
make jupyter
```

Access at http://localhost:8888 (token: pipeline)

#### Monitoring Stack

For observing application behavior:

```bash
make monitoring
```

- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (admin:admin)

## Code Organization

### Project Structure

```
src/pipeline/
├── core/          # Core business logic
│   └── pipeline.py
├── data/          # Data processing
│   └── processor.py
├── config/        # Configuration management
│   └── settings.py
└── utils/         # Utility functions
    └── logging.py
```

### Adding New Features

1. **Create a new branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Write your code** following the existing patterns

3. **Add tests** for your new functionality

4. **Update documentation** if necessary

5. **Run quality checks:**
   ```bash
   make audit
   ```

6. **Commit and push:**
   ```bash
   git add .
   git commit -m "Add your feature description"
   git push origin feature/your-feature-name
   ```

## Configuration Management

### Environment Variables

Copy the example environment file and customize:

```bash
cp .env.example .env
```

Edit `.env` with your specific values.

### Settings Classes

Configuration is managed through Pydantic settings classes in `src/pipeline/config/settings.py`. This provides:

- Type validation
- Environment variable loading
- Nested configuration sections
- IDE support with autocomplete

### Adding New Configuration

1. Add the setting to the appropriate settings class
2. Update `.env.example` with the new variable
3. Update documentation if the setting affects user behavior

## Debugging

### Local Debugging

Use your IDE's debugger or add breakpoints:

```python
import pdb; pdb.set_trace()
```

### Docker Debugging

Debug inside containers:

```bash
# Start container with debugging enabled
docker-compose run --rm pipeline bash

# Or attach to running container
make docker-shell
```

### Logging

The application uses structured logging. Add debug information:

```python
import structlog

logger = structlog.get_logger()
logger.debug("Debug information", extra_field="value")
```

## Performance Considerations

### Profiling

Profile your code to identify bottlenecks:

```bash
# Add to your code
import cProfile
cProfile.run('your_function()')

# Or use line_profiler
pip install line_profiler
kernprof -l -v your_script.py
```

### Async Code

The application supports async/await patterns. Use them for I/O operations:

```python
async def async_operation():
    # Use httpx instead of requests
    async with httpx.AsyncClient() as client:
        response = await client.get("http://example.com")
    return response
```

## Troubleshooting

### Common Issues

1. **Poetry installation issues:**
   ```bash
   # Clear cache and reinstall
   poetry cache clear --all pypi
   poetry install
   ```

2. **Docker permission issues:**
   ```bash
   # Add user to docker group (Linux)
   sudo usermod -aG docker $USER
   ```

3. **Database connection issues:**
   ```bash
   # Check if services are running
   docker-compose ps
   
   # Check logs
   docker-compose logs postgres
   ```

4. **Port conflicts:**
   ```bash
   # Check what's using the port
   lsof -i :8000
   
   # Kill the process or change ports in docker-compose.yml
   ```

### Getting Help

- Check the [GitHub Issues](https://github.com/username/pipeline/issues)
- Review the existing tests for usage examples
- Look at the configuration classes for available options
- Consult the Docker Compose file for service configurations

## Contributing Guidelines

Please see [CONTRIBUTING.md](contributing.md) for detailed contribution guidelines.

Remember to:
- Follow the code style guidelines
- Write tests for new functionality  
- Update documentation
- Keep commits focused and descriptive
- Ensure CI passes before submitting PRs
