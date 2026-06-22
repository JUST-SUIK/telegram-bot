"""Natural language handler for Telegram Bot Agent."""

import json
import logging
from telegram import Update
from telegram.ext import ContextTypes
from openai import OpenAI
import os

logger = logging.getLogger(__name__)

# System prompt for intent recognition
INTENT_RECOGNITION_PROMPT = """你是一个意图识别助手。用户会发送自然语言消息，你需要识别用户的意图并返回 JSON 格式的结果。

可能的意图：
1. "screenshot" - 截图相关（截图、截屏、屏幕截图、看看屏幕、给我看看当前画面）
2. "status" - 状态查询（查看状态、进程状态、运行情况、CPU、内存、电脑在做什么、系统状态）
3. "list" - 列出进程（列出进程、查看进程、有哪些程序在运行、正在运行什么）
4. "click" - 点击操作（点击、按按钮、选择）
5. "type" - 输入操作（输入、打字、填写）
6. "key" - 按键操作（按下、按键、回车、确认）
7. "exec" - 执行命令（执行、运行、命令）
8. "ask" - AI问答（问、询问、问题、帮我看看、解释）
9. "help" - 帮助（帮助、怎么用、有什么功能）
10. "chat" - 普通聊天（其他所有消息）

返回格式（严格 JSON）：
{
    "intent": "意图名称",
    "params": "参数（如果有）",
    "response": "友好的确认消息（如果是操作类意图）"
}

示例：
用户："帮我截图" -> {"intent": "screenshot", "params": "", "response": "好的，正在为你截图..."}
用户："看看屏幕" -> {"intent": "screenshot", "params": "", "response": "好的，正在截图..."}
用户："查看状态" -> {"intent": "status", "params": "", "response": "好的，正在查询状态..."}
用户："我的电脑目前在做什么工作？" -> {"intent": "status", "params": "", "response": "好的，正在查询电脑状态..."}
用户："电脑在运行什么？" -> {"intent": "status", "params": "", "response": "好的，正在查询运行中的程序..."}
用户："有什么程序在运行" -> {"intent": "list", "params": "", "response": "好的，正在列出运行中的程序..."}
用户："正在运行什么程序？" -> {"intent": "list", "params": "", "response": "好的，正在列出运行中的程序..."}
用户："点击确认按钮" -> {"intent": "click", "params": "确认按钮", "response": "好的，正在点击确认按钮..."}
用户："输入 hello" -> {"intent": "type", "params": "hello", "response": "好的，正在输入 hello..."}
用户："按下回车" -> {"intent": "key", "params": "enter", "response": "好的，正在按下回车键..."}
用户："执行 dir 命令" -> {"intent": "exec", "params": "dir", "response": "好的，正在执行 dir 命令..."}
用户："什么是 Python" -> {"intent": "ask", "params": "什么是 Python", "response": "好的，正在向 AI 提问..."}
用户："你好" -> {"intent": "chat", "params": "", "response": ""}

重要规则：
1. 只返回 JSON，不要有其他内容
2. response 字段只用于操作类意图，聊天意图留空
3. 如果用户询问电脑状态、运行情况、正在做什么等，必须识别为 "status" 或 "list" 意图，绝对不能识别为 "chat"
4. 只有真正的闲聊（如"你好"、"今天天气怎么样"）才识别为 "chat"
"""

def recognize_intent(message: str) -> dict:
    """Recognize user intent from natural language message.

    Args:
        message: User's message

    Returns:
        dict: Intent recognition result
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
                {"role": "system", "content": INTENT_RECOGNITION_PROMPT},
                {"role": "user", "content": message}
            ],
            temperature=0.1,
            max_tokens=200
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
        return {"intent": "chat", "params": "", "response": ""}

    except Exception as e:
        logger.error(f"Intent recognition error: {e}")
        return {"intent": "chat", "params": "", "response": ""}

async def handle_natural_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle natural language messages.

    Args:
        update: Telegram update
        context: Bot context
    """
    from src.bot.utils.security import is_user_allowed

    user_id = update.message.from_user.id
    if not is_user_allowed(user_id):
        return

    message = update.message.text.strip()

    # Skip if it's a confirmation message
    if message in ['确认', '取消']:
        return

    logger.info(f"Processing natural language message from user {user_id}: {message}")

    # Recognize intent
    intent_result = recognize_intent(message)
    intent = intent_result.get('intent', 'chat')
    params = intent_result.get('params', '')
    response = intent_result.get('response', '')

    logger.info(f"Recognized intent: {intent}, params: {params}")

    # Send acknowledgment for action intents
    if response and intent != 'chat':
        await update.message.reply_text(response)

    # Execute based on intent
    if intent == 'screenshot':
        from src.bot.handlers.screenshot import screenshot_command
        await screenshot_command(update, context)

    elif intent == 'status':
        from src.bot.handlers.status import status_command
        # Set args for status command
        context.args = []
        await status_command(update, context)

    elif intent == 'list':
        from src.bot.handlers.status import list_command
        await list_command(update, context)

    elif intent == 'click':
        from src.bot.handlers.gui import click_command
        # Parse click target
        context.args = params.split() if params else []
        await click_command(update, context)

    elif intent == 'type':
        from src.bot.handlers.gui import type_command
        context.args = [params] if params else []
        await type_command(update, context)

    elif intent == 'key':
        from src.bot.handlers.gui import key_command
        context.args = [params] if params else []
        await key_command(update, context)

    elif intent == 'exec':
        from src.bot.handlers.command import exec_command
        context.args = params.split() if params else []
        await exec_command(update, context)

    elif intent == 'ask':
        from src.bot.handlers.claude import ask_command
        context.args = params.split() if params else []
        await ask_command(update, context)

    elif intent == 'help':
        help_message = (
            "📖 自然语言使用指南\n\n"
            "你可以直接用自然语言和我交流，例如：\n\n"
            "📸 截图：\n"
            "- 帮我截图\n"
            "- 看看屏幕\n"
            "- 截个屏\n\n"
            "📊 状态：\n"
            "- 查看状态\n"
            "- 有什么程序在运行\n"
            "- CPU 使用情况\n\n"
            "🖱️ 操作：\n"
            "- 点击确认按钮\n"
            "- 输入 hello\n"
            "- 按下回车\n\n"
            "💻 命令：\n"
            "- 执行 dir 命令\n"
            "- 运行 python test.py\n\n"
            "🤖 AI：\n"
            "- 什么是 Python？\n"
            "- 帮我解释这段代码\n\n"
            "或者直接输入命令：\n"
            "/screenshot, /status, /exec, /ask 等"
        )
        await update.message.reply_text(help_message)

    else:  # chat
        # For chat, call AI directly
        from src.bot.utils.config import load_config
        load_config()  # Ensure .env is loaded
        from src.bot.services.claude_cli import ask_claude
        result = ask_claude(message)
        if result['success']:
            ai_response = result['output']
            # Truncate if too long
            if len(ai_response) > 4000:
                ai_response = ai_response[:4000] + "\n\n... (回答已截断)"
            await update.message.reply_text(ai_response)
        else:
            await update.message.reply_text(f"❌ AI 调用失败: {result['error']}")