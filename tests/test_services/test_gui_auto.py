"""Tests for GUI automation service."""

import pytest
from unittest.mock import patch, MagicMock
from src.bot.services.gui_auto import click_at, type_text, press_key

def test_click_at_returns_true():
    """Test that click_at returns True on success."""
    with patch('src.bot.services.gui_auto.pyautogui') as mock_pyautogui:
        result = click_at(100, 200)
        assert result is True
        mock_pyautogui.click.assert_called_once_with(100, 200)

def test_type_text_returns_true():
    """Test that type_text returns True on success."""
    with patch('src.bot.services.gui_auto.pyautogui') as mock_pyautogui:
        result = type_text('hello')
        assert result is True
        mock_pyautogui.typewrite.assert_called_once_with('hello', interval=0.05)

def test_press_key_returns_true():
    """Test that press_key returns True on success."""
    with patch('src.bot.services.gui_auto.pyautogui') as mock_pyautogui:
        result = press_key('enter')
        assert result is True
        mock_pyautogui.press.assert_called_once_with('enter')