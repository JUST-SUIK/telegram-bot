"""Tests for exec command handler."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from telegram import Update
from telegram.ext import ContextTypes
from src.bot.handlers.command import exec_command

@pytest.mark.asyncio
async def test_exec_command_with_valid_command():
    """Test exec_command with a valid command."""
    update = MagicMock(spec=Update)
    update.message = AsyncMock()
    update.message.from_user.id = 6531095340
    context = MagicMock(spec=ContextTypes.DEFAULT_TYPE)
    context.args = ['echo', 'hello']

    with patch('src.bot.handlers.command.is_user_allowed', return_value=True), \
         patch('src.bot.handlers.command.is_command_allowed', return_value=(True, '')):
        await exec_command(update, context)

        update.message.reply_text.assert_called()

@pytest.mark.asyncio
async def test_exec_command_with_blacklisted_command():
    """Test exec_command rejects blacklisted command."""
    update = MagicMock(spec=Update)
    update.message = AsyncMock()
    update.message.from_user.id = 6531095340
    context = MagicMock(spec=ContextTypes.DEFAULT_TYPE)
    context.args = ['rm', '-rf', '/']

    with patch('src.bot.handlers.command.is_user_allowed', return_value=True), \
         patch('src.bot.handlers.command.is_command_allowed', return_value=(False, '危险命令')):
        await exec_command(update, context)

        call_args = update.message.reply_text.call_args
        assert '❌' in call_args[0][0] or '禁止' in call_args[0][0]

@pytest.mark.asyncio
async def test_exec_command_with_unauthorized_user():
    """Test exec_command rejects unauthorized user."""
    update = MagicMock(spec=Update)
    update.message = AsyncMock()
    update.message.from_user.id = 9999999999
    context = MagicMock(spec=ContextTypes.DEFAULT_TYPE)
    context.args = ['echo', 'hello']

    with patch('src.bot.handlers.command.is_user_allowed', return_value=False):
        await exec_command(update, context)

        call_args = update.message.reply_text.call_args
        assert '❌' in call_args[0][0] or '权限' in call_args[0][0]