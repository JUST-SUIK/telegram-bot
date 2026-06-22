"""Tests for Claude Code CLI service."""

import pytest
from unittest.mock import patch, MagicMock
from src.bot.services.claude_cli import ask_claude

def test_ask_claude_returns_dict():
    """Test that ask_claude returns a dictionary."""
    with patch('subprocess.run') as mock_run:
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout='Claude response',
            stderr=''
        )

        result = ask_claude('What is Python?')
        assert isinstance(result, dict)
        assert 'success' in result
        assert 'output' in result

def test_ask_claude_success():
    """Test successful Claude CLI call."""
    with patch('subprocess.run') as mock_run:
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout='Python is a programming language.',
            stderr=''
        )

        result = ask_claude('What is Python?')
        assert result['success'] is True
        assert 'Python' in result['output']

def test_ask_claude_with_working_dir():
    """Test Claude CLI with custom working directory."""
    with patch('subprocess.run') as mock_run:
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout='Response',
            stderr=''
        )

        result = ask_claude('test', working_dir='E:/Project')
        assert result['success'] is True