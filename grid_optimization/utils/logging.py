"""
Logging Configuration

Centralized logging setup for the grid optimization system.
"""

import logging
import sys
from pathlib import Path
from typing import Optional

from .config import get_config


def setup_logging(
    level: Optional[str] = None, log_file: Optional[str] = None, format_string: Optional[str] = None
) -> None:
    """
    Configure logging for the application.

    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Path to log file (optional)
        format_string: Custom log format (optional)
    """
    config = get_config()

    # Default values from config
    if level is None:
        level = config.log_level

    if format_string is None:
        format_string = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format=format_string,
        handlers=[logging.StreamHandler(sys.stdout)],
    )

    # Add file handler if specified
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(log_path)
        file_handler.setFormatter(logging.Formatter(format_string))
        logging.getLogger().addHandler(file_handler)

    # Set specific logger levels
    logging.getLogger("aiq").setLevel(logging.WARNING)  # Quiet AIQ logs
    logging.getLogger("urllib3").setLevel(logging.WARNING)  # Quiet HTTP logs

    logger = logging.getLogger(__name__)
    logger.info(f"Logging configured - Level: {level}, Environment: {config.environment}")


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with consistent configuration.

    Args:
        name: Logger name (usually __name__)

    Returns:
        Configured logger instance
    """
    return logging.getLogger(name)
