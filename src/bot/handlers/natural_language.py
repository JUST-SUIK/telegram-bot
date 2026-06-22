"""Natural language handler for Telegram Bot Agent."""

import json
import logging
from telegram import Update
from telegram.ext import ContextTypes
from openai import OpenAI
import os

logger = logging.getLogger(__name__)

# System prompt for AI agent
AI_AGENT_PROMPT = """你是一个电脑控制助手。用户会发送自然语言消息，你需要分析用户意图并执行相应的操作。

你可以执行以下操作（只能选择一个）：
1. screenshot - 截取电脑屏幕
2. status - 查看进程状态和系统信息
3. list - 列出所有运行中的程序
4. click <目标> - 点击屏幕上的元素
5. type <文本> - 输入文字
6. key <按键> - 按下键盘按键
7. exec <命令> - 执行系统命令
8. help - 显示帮助信息
9. chat - 普通聊天（不需要执行任何操作）

返回格式（严格 JSON）：
{
    "action": "要执行的操作",
    "params": "操作参数（如果有）",
    "response": "给用户的友好回复"
}

示例：
用户："帮我截图" -> {"action": "screenshot", "params": "", "response": "好的，正在为你截图..."}
用户："查看状态" -> {"action": "status", "params": "", "response": "好的，正在查询状态..."}
用户："我的电脑目前在做什么工作？" -> {"action": "status", "params": "", "response": "好的，正在查询电脑状态..."}
用户："有什么程序在运行" -> {"action": "list", "params": "", "response": "好的，正在列出运行中的程序..."}
用户："我的电脑现在claude code在进行哪些项目？" -> {"action": "status", "params": "", "response": "好的，正在查询 Claude Code 项目状态..."}
用户："点击确认按钮" -> {"action": "click", "params": "确认按钮", "response": "好的，正在点击确认按钮..."}
用户："输入 hello" -> {"action": "type", "params": "hello", "response": "好的，正在输入 hello..."}
用户："按下回车" -> {"action": "key", "params": "enter", "response": "好的，正在按下回车键..."}
用户："执行 dir 命令" -> {"action": "exec", "params": "dir", "response": "好的，正在执行 dir 命令..."}
用户："什么是 Python" -> {"action": "chat", "params": "", "response": "Python 是一种高级编程语言..."}
用户："你好" -> {"action": "chat", "params": "", "response": "你好！有什么我可以帮助你的吗？"}
用户："今天天气怎么样" -> {"action": "chat", "params": "", "response": "我无法查询天气，但你可以告诉我你需要什么帮助？"}

重要规则：
1. 只返回 JSON，不要有其他内容
2. 只能选择一个 action，不能多个
3. 如果用户询问电脑状态、运行情况、正在做什么等，必须执行 "status" 或 "list" 操作
4. 只有真正的闲聊才使用 "chat" 操作
5. response 字段要简洁友好，不要太长
6. 不要使用 "ask" 操作，直接回答用户问题
"""

def analyze_with_ai(message: str) -> dict:
    """Analyze user message with AI and determine action.

    Args:
        message: User's message

    Returns:
        dict: {'action': str, 'params': str, 'response': str}
    """
    api_key = os.getenv('MIMO_API_KEY')
    api_base = os.getenv('MIMO_API_BASE_URL', 'https://token-plan-cn.xiaomimimo.com/v1')

    client = OpenAI(
        api_key=api_key,
        base_url=api_base,
    )

    try:
        response = client.chat.completions.create(
            model="mimo-v2.5-pro",
            messages=[
                {"role": "system", "content": AI_AGENT_PROMPT},
                {"role": "user", "content": message}
            ],
            temperature=0.1,
            max_tokens=300
        )

        response_text = response.choices[0].message.content.strip()

        # Try to parse JSON
        try:
            # Find JSON in response
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            if json_start != -1 and json_end != -1:
                json_str = response_text[json_start:json_end]
                result = json.loads(json_str)
                return result
        except json.JSONDecodeError:
            pass

        # Default to chat if parsing fails
        return {"action": "chat", "params": "", "response": response_text}

    except Exception as e:
        logger.error(f"AI analysis error: {e}")
        return {"action": "chat", "params": "", "response": "抱歉，我暂时无法处理你的请求。"}

async def handle_natural_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle natural language messages.

    Args:
        update: Telegram update
        context: Bot context
    """
    from src.bot.utils.security import is_user_allowed
    from src.bot.utils.config import load_config

    user_id = update.message.from_user.id
    if not is_user_allowed(user_id):
        return

    message = update.message.text.strip()

    # Skip if it's a confirmation message
    if message in ['确认', '取消']:
        return

    logger.info(f"Processing natural language message from user {user_id}: {message}")

    # Load config to ensure API key is available
    load_config()

    # Analyze message with AI
    result = analyze_with_ai(message)
    action = result.get('action', 'chat')
    params = result.get('params', '')
    response = result.get('response', '')

    logger.info(f"AI analysis result: action={action}, params={params}")

    # Execute action and send response
    if action == 'screenshot':
        await update.message.reply_text(response)
        from src.bot.handlers.screenshot import screenshot_command
        await screenshot_command(update, context)

    elif action == 'status':
        await update.message.reply_text(response)
        from src.bot.handlers.status import status_command
        context.args = []
        await status_command(update, context)

    elif action == 'list':
        await update.message.reply_text(response)
        from src.bot.handlers.status import list_command
        await list_command(update, context)

    elif action == 'click':
        await update.message.reply_text(response)
        from src.bot.handlers.gui import click_command
        context.args = params.split() if params else []
        await click_command(update, context)

    elif action == 'type':
        await update.message.reply_text(response)
        from src.bot.handlers.gui import type_command
        context.args = [params] if params else []
        await type_command(update, context)

    elif action == 'key':
        await update.message.reply_text(response)
        from src.bot.handlers.gui import key_command
        context.args = [params] if params else []
        await key_command(update, context)

    elif action == 'exec':
        await update.message.reply_text(response)
        from src.bot.handlers.command import exec_command
        context.args = params.split() if params else []
        await exec_command(update, context)

    elif action == 'help':
        help_message = (
            "📖 使用帮助\n\n"
            "你可以直接用自然语言和我交流，例如：\n\n"
            "📸 截图：帮我截图、看看屏幕\n"
            "📊 状态：查看状态、电脑在做什么\n"
            "🖱️ 操作：点击确认按钮、输入 hello\n"
            "💻 命令：执行 dir 命令\n"
            "🤖 AI：什么是 Python？\n\n"
            "或者直接输入命令：\n"
            "/screenshot, /status, /exec, /ask 等"
        )
        await update.message.reply_text(help_message)

    else:  # chat
        # For chat, just send the response
        await update.message.reply_text(response)