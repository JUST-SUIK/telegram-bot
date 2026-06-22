"""Tests for ask command handler."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from telegram import Update
from telegram.ext import ContextTypes
from src.bot.handlers.claude import ask_command

@pytest.mark.asyncio
async def test_ask_command_with_question():
    """Test ask_command with a question."""
    update = MagicMock(spec=Update)
    update.message = AsyncMock()
    context = MagicMock(spec=ContextTypes.DEFAULT_TYPE)
    context.args = ['What', 'is', 'Python?']

    with patch('src.bot.handlers.claude.ask_claude', return_value={'success': True, 'output': 'Python is a language', 'error': ''}):
        await ask_command(update, context)

        update.message.reply_text.assert_called()
        call_args = update.message.reply_text.call_args
        assert 'Python' in call_args[0][0]

@pytest.mark.asyncio
async def test_ask_command_without_question():
    """Test ask_command without question."""
    update = MagicMock(spec=Update)
    update.message = AsyncMock()
    context = MagicMock(spec=ContextTypes.DEFAULT_TYPE)
    context.args = []

    await ask_command(update, context)

    call_args = update.message.reply_text.call_args
    assert '❌' in call_args[0][0] or '请提供' in call_args[0][0]