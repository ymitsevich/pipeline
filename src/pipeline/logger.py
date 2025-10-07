"""
Logging configuration for the pipeline application.
"""

import logging
import logging.config
import sys
from pythonjsonlogger import jsonlogger


def setup_logging(log_level: str = "INFO", use_json: bool = False):
    """
    Configure application logging.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        use_json: If True, output JSON logs; otherwise plain text
    """
    level = getattr(logging, log_level.upper(), logging.INFO)

    if use_json:
        formatter = jsonlogger.JsonFormatter(
            "%(asctime)s %(levelname)s %(name)s %(message)s",
            timestamp=True,
        )
    else:
        formatter = logging.Formatter(
            fmt="%(asctime)s %(levelname)-8s [%(name)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    handler.setFormatter(formatter)

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.handlers.clear()  # Remove any existing handlers
    root_logger.addHandler(handler)

    # Configure application logger
    app_logger = logging.getLogger("pipeline")
    app_logger.setLevel(level)

    return app_logger


def get_plain_text_logger(name: str) -> logging.Logger:
    """
    Get predefined plain text info logger instance for a specific module.

    Args:
        name: Logger name (typically __name__)

    Returns:
        Logger instance
    """
    logger = logging.getLogger(name)
    setup_logging(log_level="INFO", use_json=False)
    return logger


def get_json_logger(name: str) -> logging.Logger:
    """
    Get predefined plain text info logger instance for a specific module.

    Args:
        name: Logger name (typically __name__)

    Returns:
        Logger instance
    """
    logger = logging.getLogger(name)
    setup_logging(log_level="INFO", use_json=True)
    return logger
