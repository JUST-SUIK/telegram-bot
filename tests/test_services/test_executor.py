"""Tests for command executor service."""

import pytest
from unittest.mock import patch, MagicMock
from src.bot.services.executor import execute_command

def test_execute_command_returns_dict():
    """Test that execute_command returns a dictionary."""
    result = execute_command('echo hello')
    assert isinstance(result, dict)
    assert 'success' in result
    assert 'output' in result
    assert 'error' in result

def test_execute_command_success():
    """Test successful command execution."""
    result = execute_command('echo hello')
    assert result['success'] is True
    assert 'hello' in result['output']

def test_execute_command_failure():
    """Test failed command execution."""
    result = execute_command('nonexistent_command_12345')
    assert result['success'] is False
    assert result['error'] != ''

def test_execute_command_timeout():
    """Test command timeout."""
    # Use Python sleep for cross-platform compatibility
    result = execute_command('python -c "import time; time.sleep(10)"', timeout=1)
    assert result['success'] is False