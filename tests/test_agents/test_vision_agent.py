"""Tests for vision agent."""

import pytest
from unittest.mock import patch, MagicMock
from src.bot.agents.vision_agent import identify_element

def test_identify_element_returns_dict():
    """Test that identify_element returns a dictionary."""
    with patch('src.bot.agents.vision_agent.call_mimo_vision') as mock_call:
        mock_call.return_value = {'found': True, 'x': 100, 'y': 200, 'confidence': 0.95}

        result = identify_element(b'fake_screenshot', '确认按钮')
        assert isinstance(result, dict)
        assert 'found' in result
        assert 'x' in result
        assert 'y' in result

def test_identify_element_found():
    """Test identify_element when element is found."""
    with patch('src.bot.agents.vision_agent.call_mimo_vision') as mock_call:
        mock_call.return_value = {'found': True, 'x': 100, 'y': 200, 'confidence': 0.95}

        result = identify_element(b'fake_screenshot', '确认按钮')
        assert result['found'] is True
        assert result['x'] == 100
        assert result['y'] == 200

def test_identify_element_not_found():
    """Test identify_element when element is not found."""
    with patch('src.bot.agents.vision_agent.call_mimo_vision') as mock_call:
        mock_call.return_value = {'found': False, 'x': 0, 'y': 0, 'confidence': 0.0}

        result = identify_element(b'fake_screenshot', '不存在的按钮')
        assert result['found'] is False