"""Tests for GUI command handlers."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from telegram import Update
from telegram.ext import ContextTypes
from src.bot.handlers.gui import click_command, type_command, key_command

@pytest.mark.asyncio
async def test_click_command_with_target():
    """Test click_command with target description."""
    update = MagicMock(spec=Update)
    update.message = AsyncMock()
    context = MagicMock(spec=ContextTypes.DEFAULT_TYPE)
    context.args = ['确认', '按钮']

    with patch('src.bot.handlers.gui.take_screenshot', return_value=b'fake_screenshot'), \
         patch('src.bot.handlers.gui.identify_element', return_value={'found': True, 'x': 100, 'y': 200, 'confidence': 0.95}), \
         patch('src.bot.handlers.gui.click_at', return_value=True):
        await click_command(update, context)

        update.message.reply_text.assert_called()

@pytest.mark.asyncio
async def test_type_command():
    """Test type_command."""
    update = MagicMock(spec=Update)
    update.message = AsyncMock()
    context = MagicMock(spec=ContextTypes.DEFAULT_TYPE)
    context.args = ['hello', 'world']

    with patch('src.bot.handlers.gui.type_text', return_value=True):
        await type_command(update, context)

        update.message.reply_text.assert_called()

@pytest.mark.asyncio
async def test_key_command():
    """Test key_command."""
    update = MagicMock(spec=Update)
    update.message = AsyncMock()
    context = MagicMock(spec=ContextTypes.DEFAULT_TYPE)
    context.args = ['enter']

    with patch('src.bot.handlers.gui.press_key', return_value=True):
        await key_command(update, context)

        update.message.reply_text.assert_called()