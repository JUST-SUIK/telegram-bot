"""Tests for bot main entry."""

import pytest
from unittest.mock import patch, MagicMock
from src.bot.main import create_application

def test_create_application_returns_application():
    """Test that create_application returns Application instance."""
    with patch('src.bot.main.load_config') as mock_config:
        mock_config.return_value = {
            'telegram': {
                'token': 'test_token',
                'allowed_users': [123456],
                'proxy': {'enabled': False}
            }
        }
        app = create_application()
        assert app is not None

def test_create_application_registers_status_handlers():
    """Test that create_application registers status handlers."""
    with patch('src.bot.main.load_config') as mock_config:
        mock_config.return_value = {
            'telegram': {
                'token': 'test_token',
                'allowed_users': [123456],
                'proxy': {'enabled': False}
            }
        }
        app = create_application()
        # Check that handlers are registered
        handlers = app.handlers
        assert len(handlers) > 0