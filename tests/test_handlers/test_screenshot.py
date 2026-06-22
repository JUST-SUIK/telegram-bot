"""Tests for screenshot command handler."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from telegram import Update
from telegram.ext import ContextTypes
from src.bot.handlers.screenshot import screenshot_command

@pytest.mark.asyncio
async def test_screenshot_command_sends_photo():
    """Test that screenshot_command sends a photo."""
    update = MagicMock(spec=Update)
    update.message = AsyncMock()
    context = MagicMock(spec=ContextTypes.DEFAULT_TYPE)

    with patch('src.bot.handlers.screenshot.take_screenshot', return_value=b'fake_png_data'):
        await screenshot_command(update, context)

        update.message.reply_photo.assert_called_once()