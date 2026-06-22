"""Command execution handler for Telegram Bot."""

from telegram import Update
from telegram.ext import ContextTypes
from src.bot.services.executor import execute_command
from src.bot.utils.security import is_user_allowed, is_command_allowed

async def exec_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /exec command - execute system command.

    Usage:
        /exec <command> - Execute a system command

    Security:
        - Checks user whitelist
        - Checks command blacklist
        - Requires confirmation for dangerous commands
    """
    user_id = update.message.from_user.id

    # Check user authorization
    if not is_user_allowed(user_id):
        await update.message.reply_text("❌ 权限不足：您没有使用此机器人的权限")
        return

    # Check if command is provided
    if not context.args:
        await update.message.reply_text("❌ 请提供要执行的命令\n用法: /exec <命令>")
        return

    command = ' '.join(context.args)

    # Check command blacklist
    allowed, reason = is_command_allowed(command)
    if not allowed:
        await update.message.reply_text(f"❌ 命令被拒绝\n\n{reason}")
        return

    # Execute command
    await update.message.reply_text(f"⏳ 正在执行命令: {command}")

    result = execute_command(command)

    if result['success']:
        message = f"✅ 命令执行成功\n\n"
        if result['output']:
            message += f"输出:\n{result['output']}"
    else:
        message = f"❌ 命令执行失败\n\n"
        if result['error']:
            message += f"错误:\n{result['error']}"

    # Truncate long messages
    if len(message) > 4000:
        message = message[:4000] + "\n\n... (输出已截断)"

    await update.message.reply_text(message)