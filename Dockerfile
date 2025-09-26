# Use Python 3.11 slim image as base
FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Create non-root user
RUN groupadd -r pipeline && useradd -r -g pipeline pipeline

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        git \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
ENV POETRY_HOME="/opt/poetry" \
    POETRY_CACHE_DIR=/tmp/poetry_cache
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="$POETRY_HOME/bin:$PATH"

# Configure Poetry
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VENV_IN_PROJECT=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

# Set work directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml poetry.lock* ./

# Development stage
FROM base as development

# Install dependencies including dev dependencies
RUN poetry install --with dev,test && rm -rf $POETRY_CACHE_DIR

# Copy source code
COPY --chown=pipeline:pipeline . .

# Switch to non-root user
USER pipeline

# Default command for development
CMD ["poetry", "run", "pipeline", "--help"]

# Production stage
FROM base as production

# Install only production dependencies
RUN poetry install --only=main && rm -rf $POETRY_CACHE_DIR

# Copy source code
COPY --chown=pipeline:pipeline src/ ./src/
COPY --chown=pipeline:pipeline README.md ./

# Install the package
RUN poetry install --only-root

# Switch to non-root user
USER pipeline

# Create directories for data and logs
RUN mkdir -p /app/data /app/logs

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD poetry run pipeline health || exit 1

# Default command
CMD ["poetry", "run", "pipeline", "run"]

# Testing stage
FROM development as testing

# Run tests
RUN poetry run pytest

# Linting stage  
FROM development as linting

# Run linting
RUN poetry run black --check . \
    && poetry run isort --check-only . \
    && poetry run flake8 . \
    && poetry run mypy src/
