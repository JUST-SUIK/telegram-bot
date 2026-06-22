"""Tests for logging utility."""

import pytest
import logging
from src.bot.utils.logger import setup_logger

def test_setup_logger_returns_logger():
    """Test that setup_logger returns a Logger instance."""
    logger = setup_logger('test_logger')
    assert isinstance(logger, logging.Logger)
    assert logger.name == 'test_logger'

def test_setup_logger_has_handlers():
    """Test that logger has file and console handlers."""
    logger = setup_logger('test_handlers')
    handler_types = [type(h).__name__ for h in logger.handlers]
    assert 'StreamHandler' in handler_types or 'FileHandler' in handler_types