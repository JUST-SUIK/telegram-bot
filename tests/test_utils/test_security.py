"""Tests for security utilities."""

import pytest
import os
from unittest.mock import patch
from src.bot.utils.security import is_user_allowed, is_command_allowed, COMMAND_BLACKLIST

def test_is_user_allowed_for_valid_user():
    """Test that allowed user ID returns True."""
    with patch.dict(os.environ, {'ALLOWED_USER_IDS': '6531095340'}):
        assert is_user_allowed(6531095340) is True

def test_is_user_allowed_for_invalid_user():
    """Test that non-allowed user ID returns False."""
    with patch.dict(os.environ, {'ALLOWED_USER_IDS': '6531095340'}):
        assert is_user_allowed(9999999999) is False

def test_is_command_allowed_for_safe_command():
    """Test that safe command returns (True, '')."""
    allowed, reason = is_command_allowed('dir')
    assert allowed is True
    assert reason == ''

def test_is_command_allowed_for_blacklisted_command():
    """Test that blacklisted command returns (False, reason)."""
    allowed, reason = is_command_allowed('rm -rf /')
    assert allowed is False
    assert 'rm -rf' in reason.lower() or '删除' in reason

def test_command_blacklist_contains_dangerous_commands():
    """Test that blacklist contains expected dangerous commands."""
    assert 'rm -rf' in COMMAND_BLACKLIST
    assert 'format' in COMMAND_BLACKLIST
    assert 'shutdown' in COMMAND_BLACKLIST