"""Logging configuration for the application."""

import logging


def configure_logging(level: str = "INFO") -> None:
    """Configure Python logging with a concise structured format."""
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

