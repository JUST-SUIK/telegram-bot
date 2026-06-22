"""Security utilities for Telegram Bot Agent."""

import os
import re
from typing import List

# Command blacklist - these commands are forbidden
COMMAND_BLACKLIST = [
    'rm -rf',
    'rm -rf /',
    'format',
    'shutdown',
    'del /f /s /q',
    'taskkill /f',
    'rmdir /s /q',
    'rd /s /q',
    'diskpart',
    'reg delete',
    'regedit',
    'bcdedit',
    'cipher /w',
]

# Risk descriptions for blacklisted commands
COMMAND_RISKS = {
    'rm -rf': '此命令会递归删除文件系统，可能导致数据丢失',
    'rm -rf /': '此命令会删除系统所有文件，导致系统崩溃',
    'format': '此命令会格式化磁盘，导致所有数据丢失',
    'shutdown': '此命令会关闭计算机，中断所有运行中的任务',
    'del /f /s /q': '此命令会强制删除目录及所有内容',
    'taskkill /f': '此命令会强制结束进程，可能导致数据丢失',
    'rmdir /s /q': '此命令会删除目录及所有内容',
    'rd /s /q': '此命令会删除目录及所有内容',
    'diskpart': '此命令会操作磁盘分区，可能导致数据丢失',
    'reg delete': '此命令会删除注册表项，可能导致系统不稳定',
    'regedit': '此命令会打开注册表编辑器，可能导致系统不稳定',
    'bcdedit': '此命令会修改启动配置，可能导致系统无法启动',
    'cipher /w': '此命令会擦除磁盘空闲空间，可能导致数据恢复困难',
}

def get_allowed_users() -> List[int]:
    """Get list of allowed user IDs from environment variable.

    Returns:
        List[int]: List of allowed user IDs
    """
    allowed_users_str = os.getenv('ALLOWED_USER_IDS', '')
    if not allowed_users_str:
        return []
    return [int(uid.strip()) for uid in allowed_users_str.split(',') if uid.strip()]

def is_user_allowed(user_id: int) -> bool:
    """Check if user ID is in whitelist.

    Args:
        user_id: Telegram user ID

    Returns:
        bool: True if user is allowed
    """
    allowed_users = get_allowed_users()
    return user_id in allowed_users

def is_command_allowed(command: str) -> tuple[bool, str]:
    """Check if command is allowed (not in blacklist).

    Args:
        command: Command to check

    Returns:
        tuple: (is_allowed: bool, reason: str)
    """
    # Normalize whitespace to prevent bypass via tabs/multiple spaces
    command_normalized = re.sub(r'\s+', ' ', command.lower().strip())

    for blacklisted in COMMAND_BLACKLIST:
        blacklisted_normalized = re.sub(r'\s+', ' ', blacklisted.lower())
        if blacklisted_normalized in command_normalized:
            risk = COMMAND_RISKS.get(blacklisted, '此命令已被列入黑名单，禁止执行')
            return False, f'命令包含禁止操作: {blacklisted}\n风险: {risk}'

    return True, ''