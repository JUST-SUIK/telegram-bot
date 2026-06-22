"""Tests for status command handler."""

import pytest
from unittest.mock import AsyncMock, MagicMock
from telegram import Update
from telegram.ext import ContextTypes
from src.bot.handlers.status import status_command, list_command

@pytest.mark.asyncio
async def test_status_command_sends_message():
    """Test that status_command sends a message."""
    update = MagicMock(spec=Update)
    update.message = AsyncMock()
    context = MagicMock(spec=ContextTypes.DEFAULT_TYPE)
    context.args = []  # No arguments, show all processes

    await status_command(update, context)

    update.message.reply_text.assert_called_once()
    call_args = update.message.reply_text.call_args
    assert '进程' in call_args[0][0] or '运行' in call_args[0][0]

@pytest.mark.asyncio
async def test_list_command_sends_message():
    """Test that list_command sends a message."""
    update = MagicMock(spec=Update)
    update.message = AsyncMock()
    context = MagicMock(spec=ContextTypes.DEFAULT_TYPE)

    await list_command(update, context)

    update.message.reply_text.assert_called_once()