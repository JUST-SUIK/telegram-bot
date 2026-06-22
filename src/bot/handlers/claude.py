"""Claude Code CLI command handler for Telegram Bot."""

from telegram import Update
from telegram.ext import ContextTypes
from src.bot.services.claude_cli import ask_claude

async def ask_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /ask command - ask Claude a question.

    Usage:
        /ask <question> - Ask Claude a question

    Examples:
        /ask What is Python?
        /ask 解释这段代码的作用
        /ask telegram-bot 这个项目有什么问题？
    """
    if not context.args:
        await update.message.reply_text(
            "❌ 请提供问题\n"
            "用法: /ask <问题>\n\n"
            "示例:\n"
            "/ask What is Python?\n"
            "/ask 解释这段代码的作用"
        )
        return

    # Parse arguments
    args = context.args
    working_dir = None

    # Check if first argument is a project name
    if len(args) > 1:
        # Try to find project directory
        import os
        projects_dir = 'E:/Project'
        potential_project = args[0]

        # Check if it's a valid project directory
        project_path = os.path.join(projects_dir, potential_project)
        if os.path.isdir(project_path):
            working_dir = project_path
            args = args[1:]  # Remove project name from args

    question = ' '.join(args)

    await update.message.reply_text(f"🤖 正在向 Claude 提问...")

    result = ask_claude(question, working_dir)

    if result['success']:
        message = f"💬 Claude 回答:\n\n{result['output']}"
    else:
        message = f"❌ Claude 调用失败\n\n{result['error']}"

    # Truncate long messages
    if len(message) > 4000:
        message = message[:4000] + "\n\n... (回答已截断)"

    await update.message.reply_text(message)