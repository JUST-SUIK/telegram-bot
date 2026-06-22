"""Tests for security utilities."""

import pytest
import os
import re
from unittest.mock import patch
from src.bot.utils.security import is_user_allowed, is_command_allowed, COMMAND_BLACKLIST, get_allowed_users

def test_is_user_allowed_for_valid_user():
    """Test that allowed user ID returns True."""
    with patch.dict(os.environ, {'ALLOWED_USER_IDS': '6531095340'}):
        assert is_user_allowed(6531095340) is True

def test_is_user_allowed_for_invalid_user():
    """Test that non-allowed user ID returns False."""
    with patch.dict(os.environ, {'ALLOWED_USER_IDS': '6531095340'}):
        assert is_user_allowed(9999999999) is False

def test_is_user_allowed_for_empty_whitelist():
    """Test that empty whitelist denies all users."""
    with patch.dict(os.environ, {'ALLOWED_USER_IDS': ''}):
        assert is_user_allowed(6531095340) is False

def test_get_allowed_users_returns_list():
    """Test that get_allowed_users returns a list."""
    with patch.dict(os.environ, {'ALLOWED_USER_IDS': '123,456,789'}):
        users = get_allowed_users()
        assert isinstance(users, list)
        assert users == [123, 456, 789]

def test_get_allowed_users_handles_empty():
    """Test that get_allowed_users handles empty string."""
    with patch.dict(os.environ, {'ALLOWED_USER_IDS': ''}):
        users = get_allowed_users()
        assert users == []

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

def test_command_blacklist_whitespace_bypass():
    """Test that whitespace manipulation cannot bypass blacklist."""
    # These should all be blocked
    test_cases = [
        'rm  -rf',  # double space
        'rm\t-rf',  # tab
        'rm -rf /',  # with path
        'rm   -rf   /',  # multiple spaces
    ]
    for cmd in test_cases:
        allowed, reason = is_command_allowed(cmd)
        assert allowed is False, f"Command '{cmd}' should be blocked but was allowed"

def test_command_blacklist_case_insensitive():
    """Test that blacklist is case-insensitive."""
    test_cases = ['RM -RF', 'Format', 'SHUTDOWN']
    for cmd in test_cases:
        allowed, reason = is_command_allowed(cmd)
        assert allowed is False, f"Command '{cmd}' should be blocked but was allowed"

def test_command_blacklist_substring_matching():
    """Test that blacklist uses substring matching."""
    # Commands containing blacklisted strings should be blocked
    test_cases = [
        'sudo rm -rf /',
        'echo test && shutdown -s',
        'del /f /s /q C:\\',
    ]
    for cmd in test_cases:
        allowed, reason = is_command_allowed(cmd)
        assert allowed is False, f"Command '{cmd}' should be blocked but was allowed"