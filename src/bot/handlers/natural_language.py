"""Natural language handler for Telegram Bot Agent."""

import json
import logging
from telegram import Update
from telegram.ext import ContextTypes
from openai import OpenAI
import os

logger = logging.getLogger(__name__)

# System prompt for AI agent
AI_AGENT_PROMPT = """你是一个电脑远程控制助手。用户通过 Telegram 给你发消息，你需要分析用户意图并执行相应的操作。

你可以执行以下操作（只能选择一个）：
1. screenshot - 截取电脑屏幕（当前屏幕画面）
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

重要理解规则：
1. "打开 TIM 并截图" = 用户已经打开了 TIM，想让你截图当前屏幕，不是启动新程序
2. "截图" / "截屏" / "看看屏幕" = screenshot 操作
3. "打开 xxx" 通常 = 用户已经在用，想让你截图看看，或切换到那个窗口
4. "看看 xxx 在干嘛" = 截图操作（screenshot）
5. "运行 xxx" / "执行 xxx" = exec 操作
6. "列出进程" / "有什么程序" = list 操作
7. "查看状态" / "电脑怎么样" = status 操作

示例：
用户："帮我截图" -> {"action": "screenshot", "params": "", "response": "好的，正在截图..."}
用户："看看屏幕" -> {"action": "screenshot", "params": "", "response": "好的，正在截图..."}
用户："打开 TIM 并截图" -> {"action": "screenshot", "params": "", "response": "好的，正在为你截图当前屏幕..."}
用户："看看我的 TIM" -> {"action": "screenshot", "params": "", "response": "好的，正在截图..."}
用户："查看状态" -> {"action": "status", "params": "", "response": "好的，正在查询状态..."}
用户："有什么程序在运行" -> {"action": "list", "params": "", "response": "好的，正在列出运行中的程序..."}
用户："点击确认按钮" -> {"action": "click", "params": "确认按钮", "response": "好的，正在点击确认按钮..."}
用户："输入 hello" -> {"action": "type", "params": "hello", "response": "好的，正在输入 hello..."}
用户："执行 dir 命令" -> {"action": "exec", "params": "dir", "response": "好的，正在执行 dir 命令..."}
用户："什么是 Python" -> {"action": "chat", "params": "", "response": "Python 是一种高级编程语言..."}
用户："你好" -> {"action": "chat", "params": "", "response": "你好！有什么我可以帮助你的吗？"}

重要规则：
1. 只返回 JSON，不要有其他内容
2. 只能选择一个 action，不能多个
3. "打开 xxx 并截图" / "看看 xxx" = screenshot（不要尝试启动程序）
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

    logger.info(f"[AI] 开始分析消息: {message}")
    logger.info(f"[AI] API Base: {api_base}")
    logger.info(f"[AI] API Key: {api_key[:10]}..." if api_key else "[AI] API Key: 未设置")

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
        logger.info(f"[AI] 原始响应: {response_text}")

        # Try to parse JSON
        try:
            # Find JSON in response
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            if json_start != -1 and json_end != -1:
                json_str = response_text[json_start:json_end]
                result = json.loads(json_str)
                logger.info(f"[AI] 解析结果: {result}")
                return result
        except json.JSONDecodeError as e:
            logger.warning(f"[AI] JSON 解析失败: {e}")

        # Default to chat if parsing fails
        logger.info(f"[AI] 使用默认 chat 响应")
        return {"action": "chat", "params": "", "response": response_text}

    except Exception as e:
        logger.error(f"[AI] 分析失败: {type(e).__name__}: {e}")
        # Return a more helpful error message
        error_msg = str(e)
        if "api_key" in error_msg.lower() or "auth" in error_msg.lower() or "401" in error_msg:
            return {"action": "chat", "params": "", "response": "❌ API Key 配置错误，请在 GUI 配置中更新 MIMO_API_KEY"}
        elif "timeout" in error_msg.lower():
            return {"action": "chat", "params": "", "response": "⏰ AI 服务响应超时，请稍后再试"}
        elif "connection" in error_msg.lower():
            return {"action": "chat", "params": "", "response": "🔌 无法连接到 AI 服务，请检查网络和代理配置"}
        else:
            return {"action": "chat", "params": "", "response": f"❌ AI 处理失败: {error_msg[:100]}"}

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
        logger.warning(f"[NL] 未授权用户 {user_id} 尝试访问")
        return

    message = update.message.text.strip()

    # Skip if it's a confirmation message
    if message in ['确认', '取消']:
        return

    logger.info(f"[NL] ========== 收到消息 ==========")
    logger.info(f"[NL] 用户: {user_id}")
    logger.info(f"[NL] 内容: {message}")

    # Load config to ensure API key is available
    load_config()

    # Analyze message with AI
    try:
        result = analyze_with_ai(message)
        action = result.get('action', 'chat')
        params = result.get('params', '')
        response = result.get('response', '')

        logger.info(f"[NL] AI 决定: action={action}, params={params}")
        logger.info(f"[NL] 回复内容: {response}")

        # Execute action and send response
        if action == 'screenshot':
            logger.info(f"[NL] 执行截图操作")
            await update.message.reply_text(response)
            from src.bot.handlers.screenshot import screenshot_command
            await screenshot_command(update, context)

        elif action == 'status':
            logger.info(f"[NL] 执行状态查询")
            await update.message.reply_text(response)
            from src.bot.handlers.status import status_command
            context.args = []
            await status_command(update, context)

        elif action == 'list':
            logger.info(f"[NL] 执行进程列表查询")
            await update.message.reply_text(response)
            from src.bot.handlers.status import list_command
            await list_command(update, context)

        elif action == 'click':
            logger.info(f"[NL] 执行点击操作: {params}")
            await update.message.reply_text(response)
            from src.bot.handlers.gui import click_command
            context.args = params.split() if params else []
            await click_command(update, context)

        elif action == 'type':
            logger.info(f"[NL] 执行输入操作: {params}")
            await update.message.reply_text(response)
            from src.bot.handlers.gui import type_command
            context.args = [params] if params else []
            await type_command(update, context)

        elif action == 'key':
            logger.info(f"[NL] 执行按键操作: {params}")
            await update.message.reply_text(response)
            from src.bot.handlers.gui import key_command
            context.args = [params] if params else []
            await key_command(update, context)

        elif action == 'exec':
            logger.info(f"[NL] 执行命令: {params}")
            await update.message.reply_text(response)
            from src.bot.handlers.command import exec_command
            context.args = params.split() if params else []
            await exec_command(update, context)

        elif action == 'help':
            logger.info(f"[NL] 显示帮助")
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
            logger.info(f"[NL] 普通聊天回复")
            await update.message.reply_text(response)

        logger.info(f"[NL] ========== 消息处理完成 ==========")

    except Exception as e:
        logger.error(f"[NL] 消息处理异常: {type(e).__name__}: {e}")
        await update.message.reply_text(f"❌ 处理消息时出错: {str(e)[:100]}")