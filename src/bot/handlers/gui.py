"""GUI automation command handlers for Telegram Bot."""

from telegram import Update
from telegram.ext import ContextTypes
from src.bot.services.gui_auto import click_at, type_text, press_key
from src.bot.services.screenshot import take_screenshot
from src.bot.agents.vision_agent import identify_element

async def click_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /click command - click on UI element.

    Usage:
        /click <target> - Click on element described by target
        /click <x> <y> - Click at specific coordinates

    Examples:
        /click 确认按钮
        /click 100 200
    """
    if not context.args:
        await update.message.reply_text("❌ 请提供点击目标\n用法: /click <目标> 或 /click <x> <y>")
        return

    # Check if coordinates are provided
    if len(context.args) == 2:
        try:
            x = int(context.args[0])
            y = int(context.args[1])

            await update.message.reply_text(f"🖱️ 正在点击坐标 ({x}, {y})...")

            if click_at(x, y):
                await update.message.reply_text(f"✅ 已点击坐标 ({x}, {y})")
            else:
                await update.message.reply_text(f"❌ 点击失败")

            return
        except ValueError:
            pass

    # Use AI to identify element
    target = ' '.join(context.args)

    await update.message.reply_text(f"📸 正在截图分析...")
    screenshot_bytes = take_screenshot()

    await update.message.reply_text(f"🔍 AI 识别中: 正在查找 '{target}'...")

    result = identify_element(screenshot_bytes, target)

    if result['found']:
        x, y = result['x'], result['y']
        confidence = result['confidence']

        await update.message.reply_text(
            f"🎯 找到目标\n"
            f"位置: ({x}, {y})\n"
            f"置信度: {confidence:.1%}\n\n"
            f"⚠️ 是否点击？回复 '确认' 执行"
        )

        # Store coordinates for confirmation
        context.user_data['pending_click'] = {'x': x, 'y': y}
    else:
        await update.message.reply_text(f"❌ 未找到 '{target}'，请尝试更具体的描述")

async def type_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /type command - type text.

    Usage:
        /type <text> - Type the specified text

    Examples:
        /type hello world
        /type 你好世界
    """
    if not context.args:
        await update.message.reply_text("❌ 请提供要输入的文本\n用法: /type <文本>")
        return

    text = ' '.join(context.args)

    await update.message.reply_text(f"⌨️ 正在输入: {text}")

    if type_text(text):
        await update.message.reply_text(f"✅ 已输入: {text}")
    else:
        await update.message.reply_text(f"❌ 输入失败")

async def key_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /key command - press keyboard key.

    Usage:
        /key <key> - Press the specified key

    Examples:
        /key enter
        /key tab
        /key escape
    """
    if not context.args:
        await update.message.reply_text("❌ 请提供要按下的按键\n用法: /key <按键>")
        return

    key = context.args[0].lower()

    await update.message.reply_text(f"⌨️ 正在按下: {key}")

    if press_key(key):
        await update.message.reply_text(f"✅ 已按下: {key}")
    else:
        await update.message.reply_text(f"❌ 按键失败: {key}")