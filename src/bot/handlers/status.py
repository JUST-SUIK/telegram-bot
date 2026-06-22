"""Status command handler for Telegram Bot."""

from telegram import Update
from telegram.ext import ContextTypes
from src.bot.services.process import get_process_list, get_process_status

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /status command - show process status.

    Usage:
        /status - show all monitored processes
        /status <process_name> - show specific process status
    """
    args = context.args

    if args:
        # Show specific process status
        process_name = args[0]
        status = get_process_status(process_name)

        if status:
            message = (
                f"📊 进程状态: {status['name']}\n\n"
                f"PID: {status['pid']}\n"
                f"CPU: {status['cpu']:.1f}%\n"
                f"内存: {status['memory']:.1f}%\n"
                f"状态: {status['status']}"
            )
        else:
            message = f"❌ 未找到进程: {process_name}"
    else:
        # Show all running processes summary
        processes = get_process_list()
        if processes:
            # Sort by CPU usage, show top 10
            top_processes = sorted(processes, key=lambda p: p['cpu'], reverse=True)[:10]
            message = "📊 运行中的进程 (CPU 占用前 10):\n\n"
            for proc in top_processes:
                message += f"• {proc['name']} (PID: {proc['pid']}) - CPU: {proc['cpu']:.1f}%, 内存: {proc['memory']:.1f}%\n"
        else:
            message = "📊 没有找到运行中的进程"

    await update.message.reply_text(message)

async def list_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /list command - list all running processes.

    Shows a formatted list of all running processes.
    """
    processes = get_process_list()

    if processes:
        # Group by first letter
        message = f"📋 运行中的进程 (共 {len(processes)} 个):\n\n"
        for proc in processes[:20]:  # Show first 20
            message += f"• {proc['name']} (PID: {proc['pid']})\n"

        if len(processes) > 20:
            message += f"\n... 还有 {len(processes) - 20} 个进程"
    else:
        message = "📋 没有找到运行中的进程"

    await update.message.reply_text(message)