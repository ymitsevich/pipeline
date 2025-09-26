"""
Pipeline: A modern Python data engineering application.

This package provides a foundation for building robust data engineering pipelines
with modern Python standards and best practices.
"""

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from pipeline.core.pipeline import Pipeline
from pipeline.config.settings import Settings

__all__ = ["Pipeline", "Settings"]
