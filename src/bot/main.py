"""Main entry point for Telegram Bot Agent."""

import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent
sys.path.insert(0, str(src_path))

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from src.bot.utils.config import load_config
from src.bot.utils.logger import setup_logger

logger = setup_logger(__name__)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command."""
    welcome_message = (
        "🤖 Telegram Bot Agent\n\n"
        "欢迎使用远程电脑控制机器人！\n\n"
        "可用命令：\n"
        "/start - 显示欢迎信息\n"
        "/help - 显示帮助信息\n"
        "/status - 查看进程状态\n"
        "/screenshot - 截取屏幕\n"
        "/exec <命令> - 执行命令\n"
        "/ask <问题> - AI 问答\n"
        "/monitor <进程名> - 添加监控\n"
        "/list - 列出运行中的进程\n"
    )
    await update.message.reply_text(welcome_message)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command."""
    help_message = (
        "📖 命令帮助\n\n"
        "监控命令：\n"
        "/status [进程名] - 查看进程状态\n"
        "/list - 列出所有运行中的进程\n"
        "/monitor <进程名> - 添加监控目标\n"
        "/unmonitor <进程名> - 移除监控目标\n\n"
        "操作命令：\n"
        "/screenshot [窗口名] - 截取屏幕\n"
        "/exec <命令> - 执行系统命令\n"
        "/log <进程名> [行数] - 读取日志\n\n"
        "GUI 命令：\n"
        "/click <目标> - 点击元素\n"
        "/type <文本> - 输入文本\n"
        "/key <按键> - 按下按键\n\n"
        "AI 命令：\n"
        "/ask <问题> - 向 AI 提问\n"
    )
    await update.message.reply_text(help_message)

def create_application():
    """Create and configure Telegram application.

    Returns:
        Application: Configured Telegram application
    """
    config = load_config()
    token = config['telegram']['token']

    application = ApplicationBuilder().token(token).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))

    return application

def main():
    """Main entry point for the bot."""
    logger.info("Starting Telegram Bot Agent...")

    try:
        config = load_config()

        # Check proxy configuration
        if config['telegram']['proxy']['enabled']:
            logger.info(f"Proxy enabled: {config['telegram']['proxy']['url']}")

        application = create_application()
        logger.info("Bot started successfully!")
        application.run_polling()

    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()