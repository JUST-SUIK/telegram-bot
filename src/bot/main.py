"""Main entry point for Telegram Bot Agent."""

import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent
sys.path.insert(0, str(src_path))

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from src.bot.utils.config import load_config
from src.bot.utils.logger import setup_logger
from src.bot.utils.security import is_user_allowed

# Import all handlers
from src.bot.handlers.status import status_command, list_command
from src.bot.handlers.command import exec_command
from src.bot.handlers.screenshot import screenshot_command
from src.bot.handlers.gui import click_command, type_command, key_command
from src.bot.handlers.claude import ask_command

logger = setup_logger(__name__)

# Authorization decorator for handlers
def require_auth(handler_func):
    """Decorator to check user authorization before handling command."""
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.message.from_user.id
        if not is_user_allowed(user_id):
            await update.message.reply_text("❌ 权限不足：您没有使用此机器人的权限")
            logger.warning(f"Unauthorized access attempt from user {user_id}")
            return
        return await handler_func(update, context)
    return wrapper

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command."""
    user_id = update.message.from_user.id
    if not is_user_allowed(user_id):
        await update.message.reply_text("❌ 权限不足：您没有使用此机器人的权限")
        return

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
        "/list - 列出运行中的进程\n"
        "/click <目标> - 点击元素\n"
        "/type <文本> - 输入文本\n"
        "/key <按键> - 按下按键\n"
    )
    await update.message.reply_text(welcome_message)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command."""
    user_id = update.message.from_user.id
    if not is_user_allowed(user_id):
        await update.message.reply_text("❌ 权限不足：您没有使用此机器人的权限")
        return

    help_message = (
        "📖 命令帮助\n\n"
        "监控命令：\n"
        "/status [进程名] - 查看进程状态\n"
        "/list - 列出所有运行中的进程\n\n"
        "操作命令：\n"
        "/screenshot - 截取屏幕\n"
        "/exec <命令> - 执行系统命令\n\n"
        "GUI 命令：\n"
        "/click <目标> - 点击元素\n"
        "/type <文本> - 输入文本\n"
        "/key <按键> - 按下按键\n\n"
        "AI 命令：\n"
        "/ask <问题> - 向 AI 提问\n"
    )
    await update.message.reply_text(help_message)

# Apply auth decorator to all handlers
@require_auth
async def auth_status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Authorized status command."""
    await status_command(update, context)

@require_auth
async def auth_list_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Authorized list command."""
    await list_command(update, context)

@require_auth
async def auth_exec_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Authorized exec command."""
    await exec_command(update, context)

@require_auth
async def auth_screenshot_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Authorized screenshot command."""
    await screenshot_command(update, context)

@require_auth
async def auth_click_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Authorized click command."""
    await click_command(update, context)

@require_auth
async def auth_type_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Authorized type command."""
    await type_command(update, context)

@require_auth
async def auth_key_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Authorized key command."""
    await key_command(update, context)

@require_auth
async def auth_ask_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Authorized ask command."""
    await ask_command(update, context)

async def handle_confirmation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle confirmation messages for pending operations."""
    user_id = update.message.from_user.id
    if not is_user_allowed(user_id):
        return

    text = update.message.text.strip()

    if text == '确认':
        # Check if there's a pending click operation
        if 'pending_click' in context.user_data:
            pending = context.user_data.pop('pending_click')
            x, y = pending['x'], pending['y']

            from src.bot.services.gui_auto import click_at
            if click_at(x, y):
                await update.message.reply_text(f"✅ 已点击坐标 ({x}, {y})")
            else:
                await update.message.reply_text(f"❌ 点击失败")
        else:
            await update.message.reply_text("没有待确认的操作")

    elif text == '取消':
        if 'pending_click' in context.user_data:
            context.user_data.pop('pending_click')
            await update.message.reply_text("✅ 已取消操作")
        else:
            await update.message.reply_text("没有待取消的操作")

def create_application():
    """Create and configure Telegram application.

    Returns:
        Application: Configured Telegram application
    """
    config = load_config()
    token = config['telegram']['token']

    # Configure proxy if enabled
    builder = ApplicationBuilder().token(token)

    if config['telegram']['proxy']['enabled']:
        proxy_url = config['telegram']['proxy']['url']
        builder = builder.proxy(proxy_url)
        logger.info(f"Proxy configured: {proxy_url}")

    application = builder.build()

    # Add command handlers (all with auth)
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("status", auth_status_command))
    application.add_handler(CommandHandler("list", auth_list_command))
    application.add_handler(CommandHandler("exec", auth_exec_command))
    application.add_handler(CommandHandler("screenshot", auth_screenshot_command))
    application.add_handler(CommandHandler("click", auth_click_command))
    application.add_handler(CommandHandler("type", auth_type_command))
    application.add_handler(CommandHandler("key", auth_key_command))
    application.add_handler(CommandHandler("ask", auth_ask_command))

    # Add message handler for confirmations
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_confirmation))

    return application

def main():
    """Main entry point for the bot."""
    logger.info("Starting Telegram Bot Agent...")

    try:
        config = load_config()

        # Verify proxy configuration
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