"""Screenshot command handler for Telegram Bot."""

import io
from telegram import Update
from telegram.ext import ContextTypes
from src.bot.services.screenshot import take_screenshot

async def screenshot_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /screenshot command - take and send screenshot.

    Usage:
        /screenshot - Take full screen screenshot
        /screenshot <window_name> - Take screenshot of specific window (future feature)
    """
    await update.message.reply_text("📸 正在截图...")

    try:
        screenshot_bytes = take_screenshot()

        # Send as photo
        photo_file = io.BytesIO(screenshot_bytes)
        photo_file.name = 'screenshot.png'

        await update.message.reply_photo(
            photo=photo_file,
            caption="📸 截图完成"
        )

    except Exception as e:
        await update.message.reply_text(f"❌ 截图失败: {str(e)}")