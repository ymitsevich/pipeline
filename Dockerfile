# Use Python 3.11 slim image as base
FROM python:3.11-slim AS base

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

# Set work directory
WORKDIR /app

# Copy dependency files
COPY requirements.txt requirements-dev.txt ./

# Upgrade pip, install dependencies caching layer
RUN python -m pip install --upgrade pip

# Development stage
FROM base AS development

# Install dependencies including dev dependencies
RUN pip install -r requirements-dev.txt

# Copy source code
COPY --chown=pipeline:pipeline . .

# Ensure src is importable
ENV PYTHONPATH=/app/src

# Switch to non-root user
USER pipeline

# Default command for development - keep container alive
CMD ["sleep", "infinity"]

# Production stage
FROM base AS production

# Install only production dependencies
RUN pip install -r requirements.txt

# Copy source code
COPY --chown=pipeline:pipeline src/ ./src/
COPY --chown=pipeline:pipeline README.md ./

# Ensure src importable
ENV PYTHONPATH=/app/src

# Install package if needed (editable install)
RUN pip install -e . || true

# Switch to non-root user
USER pipeline

# Create directories for data and logs
RUN mkdir -p /app/data /app/logs

# Health check - using a simple python check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import pipeline" || exit 1

# Default command
CMD ["sleep", "infinity"]

# Testing stage
FROM development AS testing

# Run tests
RUN python -m pytest

# Linting stage  
FROM development AS linting

# Run linting
RUN black --check . \
    && isort --check-only . \
    && flake8 . \
    && mypy src/
