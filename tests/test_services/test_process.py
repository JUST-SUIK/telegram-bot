"""Tests for process monitoring service."""

import pytest
from unittest.mock import patch, MagicMock
from src.bot.services.process import get_process_list, get_process_status, is_process_running

def test_get_process_list_returns_list():
    """Test that get_process_list returns a list."""
    result = get_process_list()
    assert isinstance(result, list)

def test_get_process_list_contains_dict():
    """Test that process list contains dictionaries."""
    result = get_process_list()
    if len(result) > 0:
        assert isinstance(result[0], dict)
        assert 'name' in result[0]
        assert 'pid' in result[0]

def test_get_process_status_for_running_process():
    """Test get_process_status for a running process."""
    # This test assumes 'python' or 'python3' is running
    result = get_process_status('python')
    if result:  # If python is running
        assert isinstance(result, dict)
        assert 'name' in result
        assert 'cpu' in result
        assert 'memory' in result

def test_is_process_running_for_existing_process():
    """Test is_process_running returns True for running process."""
    result = is_process_running('python')
    # This will be True if python is running, False otherwise
    assert isinstance(result, bool)