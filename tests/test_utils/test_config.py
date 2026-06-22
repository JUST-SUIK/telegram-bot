"""Tests for configuration management."""

import pytest
import os
from unittest.mock import patch
from src.bot.utils.config import load_config, get_env

def test_load_config_returns_dict():
    """Test that load_config returns a dictionary."""
    config = load_config()
    assert isinstance(config, dict)
    assert 'telegram' in config
    assert 'monitor' in config

def test_get_env_returns_value():
    """Test that get_env returns environment variable value."""
    with patch.dict(os.environ, {'TEST_VAR': 'test_value'}):
        result = get_env('TEST_VAR')
        assert result == 'test_value'

def test_get_env_returns_none_for_missing():
    """Test that get_env returns None for missing variables."""
    result = get_env('NONEXISTENT_VAR_12345')
    assert result is None