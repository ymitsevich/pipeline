"""Logging configuration and utilities."""

import json
import logging
import sys
from typing import Any, Dict, Optional

import structlog
from structlog import configure, get_logger
from structlog.processors import JSONRenderer, TimeStamper
from structlog.stdlib import add_log_level, filter_by_level


def configure_logging(
    log_level: str = "INFO",
    json_logs: bool = True,
    include_timestamp: bool = True,
) -> None:
    """Configure structured logging.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        json_logs: Whether to output logs in JSON format
        include_timestamp: Whether to include timestamps in logs
    """
    # Configure standard library logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, log_level.upper()),
    )
    
    # Build processors list
    processors = [
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
    ]
    
    if include_timestamp:
        processors.append(TimeStamper(fmt="ISO"))
    
    # Add appropriate renderer
    if json_logs:
        processors.append(JSONRenderer())
    else:
        processors.append(structlog.dev.ConsoleRenderer())
    
    # Configure structlog
    configure(
        processors=processors,
        wrapper_class=structlog.stdlib.BoundLogger,
        logger_factory=structlog.stdlib.LoggerFactory(),
        context_class=dict,
        cache_logger_on_first_use=True,
    )


def get_logger_with_context(**context: Any) -> structlog.BoundLoggerProtocol:
    """Get a logger with additional context.
    
    Args:
        **context: Additional context to bind to the logger
        
    Returns:
        Bound logger with context
    """
    logger = get_logger()
    return logger.bind(**context) if context else logger


class CorrelationIdProcessor:
    """Processor to add correlation ID to log records."""
    
    def __init__(self, correlation_id_key: str = "correlation_id") -> None:
        """Initialize the processor.
        
        Args:
            correlation_id_key: Key name for the correlation ID
        """
        self.correlation_id_key = correlation_id_key
        self._correlation_id: Optional[str] = None
    
    def set_correlation_id(self, correlation_id: str) -> None:
        """Set the correlation ID.
        
        Args:
            correlation_id: The correlation ID to set
        """
        self._correlation_id = correlation_id
    
    def __call__(
        self, logger: Any, method_name: str, event_dict: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Add correlation ID to the event dictionary.
        
        Args:
            logger: The logger instance
            method_name: The method name being called
            event_dict: The event dictionary
            
        Returns:
            Updated event dictionary with correlation ID
        """
        if self._correlation_id:
            event_dict[self.correlation_id_key] = self._correlation_id
        return event_dict
