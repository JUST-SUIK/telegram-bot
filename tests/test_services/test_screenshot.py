"""Tests for screenshot service."""

import pytest
from unittest.mock import patch, MagicMock
from src.bot.services.screenshot import take_screenshot

def test_take_screenshot_returns_bytes():
    """Test that take_screenshot returns bytes."""
    with patch('src.bot.services.screenshot.mss.mss') as mock_mss:
        mock_sct = MagicMock()
        mock_sct.shot.return_value = 'fake_screenshot.png'
        mock_mss.return_value.__enter__ = MagicMock(return_value=mock_sct)
        mock_mss.return_value.__exit__ = MagicMock()

        with patch('src.bot.services.screenshot.Image') as mock_image:
            mock_img = MagicMock()
            mock_image.open.return_value = mock_img

            result = take_screenshot()
            assert isinstance(result, bytes)

def test_take_screenshot_with_region():
    """Test take_screenshot with specific region."""
    region = {'top': 0, 'left': 0, 'width': 800, 'height': 600}

    with patch('src.bot.services.screenshot.mss.mss') as mock_mss:
        mock_sct = MagicMock()
        mock_screenshot = MagicMock()
        mock_screenshot.size = (800, 600)
        mock_screenshot.rgb = b'fake_rgb_data'
        mock_sct.grab.return_value = mock_screenshot
        mock_mss.return_value.__enter__ = MagicMock(return_value=mock_sct)
        mock_mss.return_value.__exit__ = MagicMock()

        with patch('src.bot.services.screenshot.Image') as mock_image:
            mock_img = MagicMock()
            mock_image.frombytes.return_value = mock_img

            result = take_screenshot(region)
            assert isinstance(result, bytes)