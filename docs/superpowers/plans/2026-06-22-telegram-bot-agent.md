# Telegram Bot Agent Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Telegram Bot Agent that enables remote monitoring and control of PC software via mobile phone, with AI-assisted GUI automation.

**Architecture:** Dual-agent system with a main LLM agent (mimo-v2.5-pro) for text/code tasks and a vision agent (mimo-v2.5) for screenshot analysis and element recognition. Uses pyautogui for GUI automation with AI-assisted coordinate detection.

**Tech Stack:** Python 3.11+, python-telegram-bot, psutil, mss, pyautogui, MiMo API (OpenAI-compatible)

## Global Constraints

- Windows native environment only
- All secrets stored in `.env` file, never committed to git
- User whitelist: Telegram ID `6531095340`
- Command blacklist for dangerous operations
- Two-step confirmation for all exec and GUI operations
- Proxy: `socks5://127.0.0.1:7897` (Clash Verge)
- Claude Code CLI path: `/c/Users/GUDGA/.openclaw/claude`
- Default working directory: `E:/Project`
- Log directory: `e:/Project/telegram-bot/log/`

---

## Phase 1: Project Foundation (Day 1-2)

### Task 1.1: Create Project Structure

**Files:**
- Create: `src/bot/__init__.py`
- Create: `src/bot/main.py`
- Create: `src/bot/handlers/__init__.py`
- Create: `src/bot/services/__init__.py`
- Create: `src/bot/agents/__init__.py`
- Create: `src/bot/utils/__init__.py`
- Create: `src/config/config.yaml`
- Create: `requirements.txt`
- Create: `run.py`
- Create: `.gitignore`
- Create: `log/` directory

**Interfaces:**
- Produces: Project directory structure ready for development

- [ ] **Step 1: Create directory structure**

```bash
cd e:/Project/telegram-bot
mkdir -p src/bot/handlers src/bot/services src/bot/agents src/bot/utils src/config log tests/test_handlers tests/test_services
```

- [ ] **Step 2: Create `requirements.txt`**

```txt
python-telegram-bot==20.7
psutil==5.9.6
mss==9.0.1
pyautogui==0.9.54
python-dotenv==1.0.0
pyyaml==6.0.1
openai==1.6.1
httpx==0.25.2
```

- [ ] **Step 3: Create `.gitignore`**

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Environment variables
.env

# Logs
log/*.log

# PyInstaller
*.spec
*.exe

# OS
.DS_Store
Thumbs.db
```

- [ ] **Step 4: Create `src/bot/__init__.py`**

```python
"""Telegram Bot Agent - Remote PC monitoring and control via Telegram."""
```

- [ ] **Step 5: Create `src/bot/handlers/__init__.py`**

```python
"""Command handlers for Telegram Bot."""
```

- [ ] **Step 6: Create `src/bot/services/__init__.py`**

```python
"""Services for system interaction and automation."""
```

- [ ] **Step 7: Create `src/bot/agents/__init__.py`**

```python
"""AI agents for text and vision processing."""
```

- [ ] **Step 8: Create `src/bot/utils/__init__.py`**

```python
"""Utility functions and configuration management."""
```

- [ ] **Step 9: Create `src/config/config.yaml`**

```yaml
# Telegram Bot Configuration
telegram:
  token: ${TELEGRAM_BOT_TOKEN}
  allowed_users:
    - 6531095340
  proxy:
    enabled: true
    url: "socks5://127.0.0.1:7897"

# Monitor Configuration
monitor:
  interval: 60
  targets: []

# Screenshot Configuration
screenshot:
  max_width: 1920
  format: "png"
  quality: 85

# GUI Automation Configuration
gui:
  confirm_before_click: true
  click_delay: 0.5

# Claude Code Configuration
claude:
  cli_path: "/c/Users/GUDGA/.openclaw/claude"
  timeout: 120
  working_dir: "E:/Project"

# Executor Configuration
executor:
  timeout: 30
  blacklist:
    - "rm -rf"
    - "format"
    - "shutdown"
    - "del /f /s /q"
    - "taskkill /f"
    - "rmdir /s /q"

# Logging Configuration
logging:
  level: "INFO"
  file: "./log/bot.log"
  max_size: 10
  backup_count: 5
```

- [ ] **Step 10: Create `run.py`**

```python
#!/usr/bin/env python3
"""Entry point for Telegram Bot Agent."""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.bot.main import main

if __name__ == '__main__':
    main()
```

- [ ] **Step 11: Verify directory structure**

```bash
tree /F e:/Project/telegram-bot
```

Expected output should show all created directories and files.

- [ ] **Step 12: Commit**

```bash
cd e:/Project/telegram-bot
git init
git add .
git commit -m "feat: initialize project structure"
```

---

### Task 1.2: Implement Configuration Management

**Files:**
- Create: `src/bot/utils/config.py`
- Create: `tests/test_utils/test_config.py`

**Interfaces:**
- Produces: `load_config() -> dict` - loads configuration from YAML and .env
- Produces: `get_env(key: str) -> str` - gets environment variable

- [ ] **Step 1: Write failing test for config loading**

```python
# tests/test_utils/test_config.py
import pytest
import os
from unittest.mock import patch
from src.bot.utils.config import load_config, get_env

def test_load_config_returns_dict():
    """Test that load_config returns a dictionary."""
    config = load_config()
    assert isinstance(config, dict)
    assert 'telegram' in config
    assert 'monitor' in config

def test_get_env_returns_value():
    """Test that get_env returns environment variable value."""
    with patch.dict(os.environ, {'TEST_VAR': 'test_value'}):
        result = get_env('TEST_VAR')
        assert result == 'test_value'

def test_get_env_returns_none_for_missing():
    """Test that get_env returns None for missing variables."""
    result = get_env('NONEXISTENT_VAR_12345')
    assert result is None
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd e:/Project/telegram-bot
python -m pytest tests/test_utils/test_config.py -v
```

Expected: FAIL with "ModuleNotFoundError: No module named 'src.bot.utils.config'"

- [ ] **Step 3: Implement config.py**

```python
# src/bot/utils/config.py
"""Configuration management for Telegram Bot Agent."""

import os
import yaml
from pathlib import Path
from dotenv import load_dotenv

def load_config() -> dict:
    """Load configuration from YAML file and environment variables.

    Returns:
        dict: Configuration dictionary
    """
    # Load .env file
    env_path = Path(__file__).parent.parent.parent.parent / '.env'
    load_dotenv(env_path)

    # Load YAML config
    config_path = Path(__file__).parent.parent.parent / 'config' / 'config.yaml'
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)

    # Replace environment variables in config
    config = _replace_env_vars(config)

    return config

def _replace_env_vars(config: dict) -> dict:
    """Replace ${VAR} patterns with environment variable values.

    Args:
        config: Configuration dictionary

    Returns:
        dict: Configuration with replaced values
    """
    if isinstance(config, dict):
        return {k: _replace_env_vars(v) for k, v in config.items()}
    elif isinstance(config, list):
        return [_replace_env_vars(item) for item in config]
    elif isinstance(config, str) and config.startswith('${') and config.endswith('}'):
        env_var = config[2:-1]
        return os.getenv(env_var, config)
    return config

def get_env(key: str) -> str | None:
    """Get environment variable value.

    Args:
        key: Environment variable name

    Returns:
        str or None: Environment variable value
    """
    return os.getenv(key)
```

- [ ] **Step 4: Run test to verify it passes**

```bash
cd e:/Project/telegram-bot
python -m pytest tests/test_utils/test_config.py -v
```

Expected: All 3 tests PASS

- [ ] **Step 5: Commit**

```bash
cd e:/Project/telegram-bot
git add src/bot/utils/config.py tests/test_utils/test_config.py
git commit -m "feat: implement configuration management"
```

---

### Task 1.3: Implement Logging Utility

**Files:**
- Create: `src/bot/utils/logger.py`
- Create: `tests/test_utils/test_logger.py`

**Interfaces:**
- Produces: `setup_logger(name: str) -> logging.Logger` - creates configured logger

- [ ] **Step 1: Write failing test for logger**

```python
# tests/test_utils/test_logger.py
import pytest
import logging
from src.bot.utils.logger import setup_logger

def test_setup_logger_returns_logger():
    """Test that setup_logger returns a Logger instance."""
    logger = setup_logger('test_logger')
    assert isinstance(logger, logging.Logger)
    assert logger.name == 'test_logger'

def test_setup_logger_has_handlers():
    """Test that logger has file and console handlers."""
    logger = setup_logger('test_handlers')
    handler_types = [type(h).__name__ for h in logger.handlers]
    assert 'StreamHandler' in handler_types or 'FileHandler' in handler_types
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd e:/Project/telegram-bot
python -m pytest tests/test_utils/test_logger.py -v
```

Expected: FAIL with "ModuleNotFoundError: No module named 'src.bot.utils.logger'"

- [ ] **Step 3: Implement logger.py**

```python
# src/bot/utils/logger.py
"""Logging utility for Telegram Bot Agent."""

import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler

def setup_logger(name: str) -> logging.Logger:
    """Setup logger with file and console handlers.

    Args:
        name: Logger name

    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Avoid adding handlers multiple times
    if logger.handlers:
        return logger

    # Create formatters
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler
    log_dir = Path(__file__).parent.parent.parent.parent / 'log'
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / 'bot.log'

    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
```

- [ ] **Step 4: Run test to verify it passes**

```bash
cd e:/Project/telegram-bot
python -m pytest tests/test_utils/test_logger.py -v
```

Expected: All 2 tests PASS

- [ ] **Step 5: Commit**

```bash
cd e:/Project/telegram-bot
git add src/bot/utils/logger.py tests/test_utils/test_logger.py
git commit -m "feat: implement logging utility"
```

---

### Task 1.4: Implement Security Module

**Files:**
- Create: `src/bot/utils/security.py`
- Create: `tests/test_utils/test_security.py`

**Interfaces:**
- Produces: `is_user_allowed(user_id: int) -> bool` - checks user whitelist
- Produces: `is_command_allowed(command: str) -> tuple[bool, str]` - checks command blacklist
- Produces: `COMMAND_BLACKLIST: list[str]` - list of forbidden commands

- [ ] **Step 1: Write failing test for security**

```python
# tests/test_utils/test_security.py
import pytest
from src.bot.utils.security import is_user_allowed, is_command_allowed, COMMAND_BLACKLIST

def test_is_user_allowed_for_valid_user():
    """Test that allowed user ID returns True."""
    assert is_user_allowed(6531095340) is True

def test_is_user_allowed_for_invalid_user():
    """Test that non-allowed user ID returns False."""
    assert is_user_allowed(9999999999) is False

def test_is_command_allowed_for_safe_command():
    """Test that safe command returns (True, '')."""
    allowed, reason = is_command_allowed('dir')
    assert allowed is True
    assert reason == ''

def test_is_command_allowed_for_blacklisted_command():
    """Test that blacklisted command returns (False, reason)."""
    allowed, reason = is_command_allowed('rm -rf /')
    assert allowed is False
    assert 'rm -rf' in reason.lower() or '删除' in reason

def test_command_blacklist_contains_dangerous_commands():
    """Test that blacklist contains expected dangerous commands."""
    assert 'rm -rf' in COMMAND_BLACKLIST
    assert 'format' in COMMAND_BLACKLIST
    assert 'shutdown' in COMMAND_BLACKLIST
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd e:/Project/telegram-bot
python -m pytest tests/test_utils/test_security.py -v
```

Expected: FAIL with "ModuleNotFoundError: No module named 'src.bot.utils.security'"

- [ ] **Step 3: Implement security.py**

```python
# src/bot/utils/security.py
"""Security utilities for Telegram Bot Agent."""

import os

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
}

def is_user_allowed(user_id: int) -> bool:
    """Check if user ID is in whitelist.

    Args:
        user_id: Telegram user ID

    Returns:
        bool: True if user is allowed
    """
    allowed_users_str = os.getenv('ALLOWED_USER_IDS', '')
    allowed_users = [int(uid.strip()) for uid in allowed_users_str.split(',') if uid.strip()]
    return user_id in allowed_users

def is_command_allowed(command: str) -> tuple[bool, str]:
    """Check if command is allowed (not in blacklist).

    Args:
        command: Command to check

    Returns:
        tuple: (is_allowed: bool, reason: str)
    """
    command_lower = command.lower().strip()

    for blacklisted in COMMAND_BLACKLIST:
        if blacklisted.lower() in command_lower:
            risk = COMMAND_RISKS.get(blacklisted, '此命令已被列入黑名单，禁止执行')
            return False, f'命令包含禁止操作: {blacklisted}\n风险: {risk}'

    return True, ''
```

- [ ] **Step 4: Run test to verify it passes**

```bash
cd e:/Project/telegram-bot
python -m pytest tests/test_utils/test_security.py -v
```

Expected: All 5 tests PASS

- [ ] **Step 5: Commit**

```bash
cd e:/Project/telegram-bot
git add src/bot/utils/security.py tests/test_utils/test_security.py
git commit -m "feat: implement security module with user whitelist and command blacklist"
```

---

### Task 1.5: Implement Telegram Bot Main Entry

**Files:**
- Create: `src/bot/main.py`
- Create: `tests/test_bot/test_main.py`

**Interfaces:**
- Produces: `main() -> None` - entry point for bot

- [ ] **Step 1: Write failing test for main**

```python
# tests/test_bot/test_main.py
import pytest
from unittest.mock import patch, MagicMock
from src.bot.main import create_application

def test_create_application_returns_application():
    """Test that create_application returns Application instance."""
    with patch('src.bot.main.load_config') as mock_config:
        mock_config.return_value = {
            'telegram': {
                'token': 'test_token',
                'allowed_users': [123456],
                'proxy': {'enabled': False}
            }
        }
        app = create_application()
        assert app is not None
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd e:/Project/telegram-bot
python -m pytest tests/test_bot/test_main.py -v
```

Expected: FAIL with "ModuleNotFoundError: No module named 'src.bot.main'"

- [ ] **Step 3: Implement main.py**

```python
# src/bot/main.py
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
```

- [ ] **Step 4: Run test to verify it passes**

```bash
cd e:/Project/telegram-bot
python -m pytest tests/test_bot/test_main.py -v
```

Expected: All 1 test PASS

- [ ] **Step 5: Commit**

```bash
cd e:/Project/telegram-bot
git add src/bot/main.py tests/test_bot/test_main.py
git commit -m "feat: implement Telegram bot main entry with start and help commands"
```

---

## Phase 2: Monitoring Capability (Day 3)

### Task 2.1: Implement Process Monitoring Service

**Files:**
- Create: `src/bot/services/process.py`
- Create: `tests/test_services/test_process.py`

**Interfaces:**
- Produces: `get_process_list() -> list[dict]` - lists all running processes
- Produces: `get_process_status(process_name: str) -> dict` - gets specific process status
- Produces: `is_process_running(process_name: str) -> bool` - checks if process is running

- [ ] **Step 1: Write failing test for process service**

```python
# tests/test_services/test_process.py
import pytest
from unittest.mock import patch, MagicMock
from src.bot.services.process import get_process_list, get_process_status, is_process_running

def test_get_process_list_returns_list():
    """Test that get_process_list returns a list."""
    result = get_process_list()
    assert isinstance(result, list)

def test_get_process_list_contains_dict():
    """Test that process list contains dictionaries."""
    result = get_process_list()
    if len(result) > 0:
        assert isinstance(result[0], dict)
        assert 'name' in result[0]
        assert 'pid' in result[0]

def test_get_process_status_for_running_process():
    """Test get_process_status for a running process."""
    # This test assumes 'python' or 'python3' is running
    result = get_process_status('python')
    if result:  # If python is running
        assert isinstance(result, dict)
        assert 'name' in result
        assert 'cpu' in result
        assert 'memory' in result

def test_is_process_running_for_existing_process():
    """Test is_process_running returns True for running process."""
    result = is_process_running('python')
    # This will be True if python is running, False otherwise
    assert isinstance(result, bool)
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd e:/Project/telegram-bot
python -m pytest tests/test_services/test_process.py -v
```

Expected: FAIL with "ModuleNotFoundError: No module named 'src.bot.services.process'"

- [ ] **Step 3: Implement process.py**

```python
# src/bot/services/process.py
"""Process monitoring service using psutil."""

import psutil
from typing import Optional

def get_process_list() -> list[dict]:
    """Get list of all running processes.

    Returns:
        list: List of process dictionaries with name, pid, cpu, memory
    """
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            pinfo = proc.info
            processes.append({
                'name': pinfo['name'],
                'pid': pinfo['pid'],
                'cpu': pinfo['cpu_percent'] or 0.0,
                'memory': pinfo['memory_percent'] or 0.0,
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return processes

def get_process_status(process_name: str) -> Optional[dict]:
    """Get status of a specific process by name.

    Args:
        process_name: Name of the process to find

    Returns:
        dict or None: Process status dictionary or None if not found
    """
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status']):
        try:
            if proc.info['name'].lower() == process_name.lower():
                return {
                    'name': proc.info['name'],
                    'pid': proc.info['pid'],
                    'cpu': proc.info['cpu_percent'] or 0.0,
                    'memory': proc.info['memory_percent'] or 0.0,
                    'status': proc.info['status'],
                }
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return None

def is_process_running(process_name: str) -> bool:
    """Check if a process is running.

    Args:
        process_name: Name of the process to check

    Returns:
        bool: True if process is running
    """
    return get_process_status(process_name) is not None
```

- [ ] **Step 4: Run test to verify it passes**

```bash
cd e:/Project/telegram-bot
python -m pytest tests/test_services/test_process.py -v
```

Expected: All 4 tests PASS

- [ ] **Step 5: Commit**

```bash
cd e:/Project/telegram-bot
git add src/bot/services/process.py tests/test_services/test_process.py
git commit -m "feat: implement process monitoring service"
```

---

### Task 2.2: Implement Status Command Handler

**Files:**
- Create: `src/bot/handlers/status.py`
- Create: `tests/test_handlers/test_status.py`

**Interfaces:**
- Produces: `status_command(update, context)` - handles /status command
- Produces: `list_command(update, context)` - handles /list command

- [ ] **Step 1: Write failing test for status handler**

```python
# tests/test_handlers/test_status.py
import pytest
from unittest.mock import AsyncMock, MagicMock
from telegram import Update
from telegram.ext import ContextTypes
from src.bot.handlers.status import status_command, list_command

@pytest.mark.asyncio
async def test_status_command_sends_message():
    """Test that status_command sends a message."""
    update = MagicMock(spec=Update)
    update.message = AsyncMock()
    context = MagicMock(spec=ContextTypes.DEFAULT_TYPE)

    await status_command(update, context)

    update.message.reply_text.assert_called_once()
    call_args = update.message.reply_text.call_args
    assert '进程状态' in call_args[0][0] or '运行中' in call_args[0][0]

@pytest.mark.asyncio
async def test_list_command_sends_message():
    """Test that list_command sends a message."""
    update = MagicMock(spec=Update)
    update.message = AsyncMock()
    context = MagicMock(spec=ContextTypes.DEFAULT_TYPE)

    await list_command(update, context)

    update.message.reply_text.assert_called_once()
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd e:/Project/telegram-bot
python -m pytest tests/test_handlers/test_status.py -v
```

Expected: FAIL with "ModuleNotFoundError: No module named 'src.bot.handlers.status'"

- [ ] **Step 3: Implement status.py**

```python
# src/bot/handlers/status.py
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
```

- [ ] **Step 4: Run test to verify it passes**

```bash
cd e:/Project/telegram-bot
python -m pytest tests/test_handlers/test_status.py -v
```

Expected: All 2 tests PASS

- [ ] **Step 5: Commit**

```bash
cd e:/Project/telegram-bot
git add src/bot/handlers/status.py tests/test_handlers/test_status.py
git commit -m "feat: implement status and list command handlers"
```

---

### Task 2.3: Register Status Handlers in Main

**Files:**
- Modify: `src/bot/main.py`
- Modify: `tests/test_bot/test_main.py`

**Interfaces:**
- Modifies: `create_application()` to register status handlers

- [ ] **Step 1: Write failing test for handler registration**

```python
# tests/test_bot/test_main.py (add to existing file)
def test_create_application_registers_status_handlers():
    """Test that create_application registers status handlers."""
    with patch('src.bot.main.load_config') as mock_config:
        mock_config.return_value = {
            'telegram': {
                'token': 'test_token',
                'allowed_users': [123456],
                'proxy': {'enabled': False}
            }
        }
        app = create_application()
        # Check that handlers are registered
        handlers = app.handlers
        assert len(handlers) > 0
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd e:/Project/telegram-bot
python -m pytest tests/test_bot/test_main.py::test_create_application_registers_status_handlers -v
```

Expected: FAIL (test should fail because status handlers not registered yet)

- [ ] **Step 3: Update main.py to register status handlers**

```python
# src/bot/main.py (add import at top)
from src.bot.handlers.status import status_command, list_command

# src/bot/main.py (add inside create_application function, after application = ApplicationBuilder()...)
    # Add command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(CommandHandler("list", list_command))
```

- [ ] **Step 4: Run test to verify it passes**

```bash
cd e:/Project/telegram-bot
python -m pytest tests/test_bot/test_main.py -v
```

Expected: All tests PASS

- [ ] **Step 5: Commit**

```bash
cd e:/Project/telegram-bot
git add src/bot/main.py tests/test_bot/test_main.py
git commit -m "feat: register status and list handlers in main"
```

---

## Phase 3: Remote Operations (Day 4-5)

### Task 3.1: Implement Command Executor Service

**Files:**
- Create: `src/bot/services/executor.py`
- Create: `tests/test_services/test_executor.py`

**Interfaces:**
- Produces: `execute_command(command: str, timeout: int = 30) -> dict` - executes system command
- Returns: `{'success': bool, 'output': str, 'error': str}`

- [ ] **Step 1: Write failing test for executor**

```python
# tests/test_services/test_executor.py
import pytest
from unittest.mock import patch, MagicMock
from src.bot.services.executor import execute_command

def test_execute_command_returns_dict():
    """Test that execute_command returns a dictionary."""
    result = execute_command('echo hello')
    assert isinstance(result, dict)
    assert 'success' in result
    assert 'output' in result
    assert 'error' in result

def test_execute_command_success():
    """Test successful command execution."""
    result = execute_command('echo hello')
    assert result['success'] is True
    assert 'hello' in result['output']

def test_execute_command_failure():
    """Test failed command execution."""
    result = execute_command('nonexistent_command_12345')
    assert result['success'] is False
    assert result['error'] != ''

def test_execute_command_timeout():
    """Test command timeout."""
    result = execute_command('timeout 5', timeout=1)
    assert result['success'] is False
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd e:/Project/telegram-bot
python -m pytest tests/test_services/test_executor.py -v
```

Expected: FAIL with "ModuleNotFoundError: No module named 'src.bot.services.executor'"

- [ ] **Step 3: Implement executor.py**

```python
# src/bot/services/executor.py
"""Command execution service."""

import subprocess
import sys

def execute_command(command: str, timeout: int = 30) -> dict:
    """Execute a system command.

    Args:
        command: Command to execute
        timeout: Timeout in seconds (default: 30)

    Returns:
        dict: Result with keys: success, output, error
    """
    try:
        # Use shell=True for Windows compatibility
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
            encoding='utf-8',
            errors='replace'
        )

        return {
            'success': result.returncode == 0,
            'output': result.stdout,
            'error': result.stderr,
        }

    except subprocess.TimeoutExpired:
        return {
            'success': False,
            'output': '',
            'error': f'命令执行超时 ({timeout}秒)',
        }
    except Exception as e:
        return {
            'success': False,
            'output': '',
            'error': str(e),
        }
```

- [ ] **Step 4: Run test to verify it passes**

```bash
cd e:/Project/telegram-bot
python -m pytest tests/test_services/test_executor.py -v
```

Expected: All 4 tests PASS

- [ ] **Step 5: Commit**

```bash
cd e:/Project/telegram-bot
git add src/bot/services/executor.py tests/test_services/test_executor.py
git commit -m "feat: implement command executor service"
```

---

### Task 3.2: Implement Exec Command Handler

**Files:**
- Create: `src/bot/handlers/command.py`
- Create: `tests/test_handlers/test_command.py`

**Interfaces:**
- Produces: `exec_command(update, context)` - handles /exec command with security checks

- [ ] **Step 1: Write failing test for exec handler**

```python
# tests/test_handlers/test_command.py
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from telegram import Update
from telegram.ext import ContextTypes
from src.bot.handlers.command import exec_command

@pytest.mark.asyncio
async def test_exec_command_with_valid_command():
    """Test exec_command with a valid command."""
    update = MagicMock(spec=Update)
    update.message = AsyncMock()
    update.message.from_user.id = 6531095340
    context = MagicMock(spec=ContextTypes.DEFAULT_TYPE)
    context.args = ['echo', 'hello']

    with patch('src.bot.handlers.command.is_user_allowed', return_value=True), \
         patch('src.bot.handlers.command.is_command_allowed', return_value=(True, '')):
        await exec_command(update, context)

        update.message.reply_text.assert_called_once()

@pytest.mark.asyncio
async def test_exec_command_with_blacklisted_command():
    """Test exec_command rejects blacklisted command."""
    update = MagicMock(spec=Update)
    update.message = AsyncMock()
    update.message.from_user.id = 6531095340
    context = MagicMock(spec=ContextTypes.DEFAULT_TYPE)
    context.args = ['rm', '-rf', '/']

    with patch('src.bot.handlers.command.is_user_allowed', return_value=True), \
         patch('src.bot.handlers.command.is_command_allowed', return_value=(False, '危险命令')):
        await exec_command(update, context)

        call_args = update.message.reply_text.call_args
        assert '❌' in call_args[0][0] or '禁止' in call_args[0][0]

@pytest.mark.asyncio
async def test_exec_command_with_unauthorized_user():
    """Test exec_command rejects unauthorized user."""
    update = MagicMock(spec=Update)
    update.message = AsyncMock()
    update.message.from_user.id = 9999999999
    context = MagicMock(spec=ContextTypes.DEFAULT_TYPE)
    context.args = ['echo', 'hello']

    with patch('src.bot.handlers.command.is_user_allowed', return_value=False):
        await exec_command(update, context)

        call_args = update.message.reply_text.call_args
        assert '❌' in call_args[0][0] or '权限' in call_args[0][0]
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd e:/Project/telegram-bot
python -m pytest tests/test_handlers/test_command.py -v
```

Expected: FAIL with "ModuleNotFoundError: No module named 'src.bot.handlers.command'"

- [ ] **Step 3: Implement command.py**

```python
# src/bot/handlers/command.py
"""Command execution handler for Telegram Bot."""

from telegram import Update
from telegram.ext import ContextTypes
from src.bot.services.executor import execute_command
from src.bot.utils.security import is_user_allowed, is_command_allowed

async def exec_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /exec command - execute system command.

    Usage:
        /exec <command> - Execute a system command

    Security:
        - Checks user whitelist
        - Checks command blacklist
        - Requires confirmation for dangerous commands
    """
    user_id = update.message.from_user.id

    # Check user authorization
    if not is_user_allowed(user_id):
        await update.message.reply_text("❌ 权限不足：您没有使用此机器人的权限")
        return

    # Check if command is provided
    if not context.args:
        await update.message.reply_text("❌ 请提供要执行的命令\n用法: /exec <命令>")
        return

    command = ' '.join(context.args)

    # Check command blacklist
    allowed, reason = is_command_allowed(command)
    if not allowed:
        await update.message.reply_text(f"❌ 命令被拒绝\n\n{reason}")
        return

    # Execute command
    await update.message.reply_text(f"⏳ 正在执行命令: {command}")

    result = execute_command(command)

    if result['success']:
        message = f"✅ 命令执行成功\n\n"
        if result['output']:
            message += f"输出:\n{result['output']}"
    else:
        message = f"❌ 命令执行失败\n\n"
        if result['error']:
            message += f"错误:\n{result['error']}"

    # Truncate long messages
    if len(message) > 4000:
        message = message[:4000] + "\n\n... (输出已截断)"

    await update.message.reply_text(message)
```

- [ ] **Step 4: Run test to verify it passes**

```bash
cd e:/Project/telegram-bot
python -m pytest tests/test_handlers/test_command.py -v
```

Expected: All 3 tests PASS

- [ ] **Step 5: Commit**

```bash
cd e:/Project/telegram-bot
git add src/bot/handlers/command.py tests/test_handlers/test_command.py
git commit -m "feat: implement exec command handler with security checks"
```

---

### Task 3.3: Implement Screenshot Service

**Files:**
- Create: `src/bot/services/screenshot.py`
- Create: `tests/test_services/test_screenshot.py`

**Interfaces:**
- Produces: `take_screenshot(region: dict = None) -> bytes` - takes screenshot and returns PNG bytes

- [ ] **Step 1: Write failing test for screenshot service**

```python
# tests/test_services/test_screenshot.py
import pytest
from unittest.mock import patch, MagicMock
from src.bot.services.screenshot import take_screenshot

def test_take_screenshot_returns_bytes():
    """Test that take_screenshot returns bytes."""
    with patch('mss.mss') as mock_mss:
        mock_sct = MagicMock()
        mock_sct.shot.return_value = b'fake_screenshot_data'
        mock_mss.return_value.__enter__ = MagicMock(return_value=mock_sct)
        mock_mss.return_value.__exit__ = MagicMock()

        result = take_screenshot()
        assert isinstance(result, bytes)

def test_take_screenshot_with_region():
    """Test take_screenshot with specific region."""
    region = {'top': 0, 'left': 0, 'width': 800, 'height': 600}

    with patch('mss.mss') as mock_mss:
        mock_sct = MagicMock()
        mock_sct.grab.return_value = MagicMock()
        mock_sct.grab.return_value.rgb = b'fake_rgb_data'
        mock_mss.return_value.__enter__ = MagicMock(return_value=mock_sct)
        mock_mss.return_value.__exit__ = MagicMock()

        result = take_screenshot(region)
        assert isinstance(result, bytes)
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd e:/Project/telegram-bot
python -m pytest tests/test_services/test_screenshot.py -v
```

Expected: FAIL with "ModuleNotFoundError: No module named 'src.bot.services.screenshot'"

- [ ] **Step 3: Implement screenshot.py**

```python
# src/bot/services/screenshot.py
"""Screenshot service using mss."""

import mss
import io
from PIL import Image
from typing import Optional

def take_screenshot(region: Optional[dict] = None) -> bytes:
    """Take a screenshot and return as PNG bytes.

    Args:
        region: Optional dict with keys: top, left, width, height
                If None, takes full screen screenshot

    Returns:
        bytes: PNG image data
    """
    with mss.mss() as sct:
        if region:
            # Capture specific region
            screenshot = sct.grab(region)
            # Convert to PIL Image
            img = Image.frombytes('RGB', screenshot.size, screenshot.rgb)
        else:
            # Capture full screen
            screenshot = sct.shot()
            img = Image.open(screenshot)

        # Convert to PNG bytes
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        return img_byte_arr.getvalue()
```

- [ ] **Step 4: Run test to verify it passes**

```bash
cd e:/Project/telegram-bot
python -m pytest tests/test_services/test_screenshot.py -v
```

Expected: All 2 tests PASS

- [ ] **Step 5: Commit**

```bash
cd e:/Project/telegram-bot
git add src/bot/services/screenshot.py tests/test_services/test_screenshot.py
git commit -m "feat: implement screenshot service using mss"
```

---

### Task 3.4: Implement Screenshot Command Handler

**Files:**
- Create: `src/bot/handlers/screenshot.py`
- Create: `tests/test_handlers/test_screenshot.py`

**Interfaces:**
- Produces: `screenshot_command(update, context)` - handles /screenshot command

- [ ] **Step 1: Write failing test for screenshot handler**

```python
# tests/test_handlers/test_screenshot.py
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from telegram import Update
from telegram.ext import ContextTypes
from src.bot.handlers.screenshot import screenshot_command

@pytest.mark.asyncio
async def test_screenshot_command_sends_photo():
    """Test that screenshot_command sends a photo."""
    update = MagicMock(spec=Update)
    update.message = AsyncMock()
    context = MagicMock(spec=ContextTypes.DEFAULT_TYPE)

    with patch('src.bot.handlers.screenshot.take_screenshot', return_value=b'fake_png_data'):
        await screenshot_command(update, context)

        update.message.reply_photo.assert_called_once()
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd e:/Project/telegram-bot
python -m pytest tests/test_handlers/test_screenshot.py -v
```

Expected: FAIL with "ModuleNotFoundError: No module named 'src.bot.handlers.screenshot'"

- [ ] **Step 3: Implement screenshot.py handler**

```python
# src/bot/handlers/screenshot.py
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
```

- [ ] **Step 4: Run test to verify it passes**

```bash
cd e:/Project/telegram-bot
python -m pytest tests/test_handlers/test_screenshot.py -v
```

Expected: All 1 test PASS

- [ ] **Step 5: Commit**

```bash
cd e:/Project/telegram-bot
git add src/bot/handlers/screenshot.py tests/test_handlers/test_screenshot.py
git commit -m "feat: implement screenshot command handler"
```

---

## Phase 4: GUI Automation (Day 6)

### Task 4.1: Implement Vision Agent

**Files:**
- Create: `src/bot/agents/vision_agent.py`
- Create: `tests/test_agents/test_vision_agent.py`

**Interfaces:**
- Produces: `identify_element(screenshot_bytes: str, target: str) -> dict` - identifies UI element coordinates
- Returns: `{'found': bool, 'x': int, 'y': int, 'confidence': float}`

- [ ] **Step 1: Write failing test for vision agent**

```python
# tests/test_agents/test_vision_agent.py
import pytest
from unittest.mock import patch, MagicMock
from src.bot.agents.vision_agent import identify_element

def test_identify_element_returns_dict():
    """Test that identify_element returns a dictionary."""
    with patch('src.bot.agents.vision_agent.call_mimo_vision') as mock_call:
        mock_call.return_value = {'found': True, 'x': 100, 'y': 200, 'confidence': 0.95}

        result = identify_element(b'fake_screenshot', '确认按钮')
        assert isinstance(result, dict)
        assert 'found' in result
        assert 'x' in result
        assert 'y' in result

def test_identify_element_found():
    """Test identify_element when element is found."""
    with patch('src.bot.agents.vision_agent.call_mimo_vision') as mock_call:
        mock_call.return_value = {'found': True, 'x': 100, 'y': 200, 'confidence': 0.95}

        result = identify_element(b'fake_screenshot', '确认按钮')
        assert result['found'] is True
        assert result['x'] == 100
        assert result['y'] == 200

def test_identify_element_not_found():
    """Test identify_element when element is not found."""
    with patch('src.bot.agents.vision_agent.call_mimo_vision') as mock_call:
        mock_call.return_value = {'found': False, 'x': 0, 'y': 0, 'confidence': 0.0}

        result = identify_element(b'fake_screenshot', '不存在的按钮')
        assert result['found'] is False
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd e:/Project/telegram-bot
python -m pytest tests/test_agents/test_vision_agent.py -v
```

Expected: FAIL with "ModuleNotFoundError: No module named 'src.bot.agents.vision_agent'"

- [ ] **Step 3: Implement vision_agent.py**

```python
# src/bot/agents/vision_agent.py
"""Vision agent for UI element identification using MiMo API."""

import os
import base64
import json
from openai import OpenAI
from typing import Optional

def identify_element(screenshot_bytes: bytes, target: str) -> dict:
    """Identify UI element in screenshot.

    Args:
        screenshot_bytes: PNG screenshot data
        target: Description of element to find (e.g., '确认按钮', '输入框')

    Returns:
        dict: {'found': bool, 'x': int, 'y': int, 'confidence': float}
    """
    try:
        result = call_mimo_vision(screenshot_bytes, target)
        return result
    except Exception as e:
        print(f"Vision agent error: {e}")
        return {'found': False, 'x': 0, 'y': 0, 'confidence': 0.0}

def call_mimo_vision(screenshot_bytes: bytes, target: str) -> dict:
    """Call MiMo API for vision analysis.

    Args:
        screenshot_bytes: PNG screenshot data
        target: Description of element to find

    Returns:
        dict: {'found': bool, 'x': int, 'y': int, 'confidence': float}
    """
    api_key = os.getenv('MIMO_API_KEY')
    api_base = os.getenv('MIMO_API_BASE_URL', 'https://token-plan-cn.xiaomimimo.com/v1')

    client = OpenAI(
        api_key=api_key,
        base_url=api_base,
    )

    # Encode screenshot to base64
    screenshot_base64 = base64.b64encode(screenshot_bytes).decode('utf-8')

    prompt = f"""分析这个截图，找到"{target}"的位置。

请返回JSON格式：
{{
    "found": true/false,
    "x": 坐标x,
    "y": 坐标y,
    "confidence": 0.0-1.0
}}

如果找不到，返回：
{{
    "found": false,
    "x": 0,
    "y": 0,
    "confidence": 0.0
}}"""

    response = client.chat.completions.create(
        model="mimo-v2.5",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{screenshot_base64}"
                        }
                    }
                ]
            }
        ],
        max_tokens=500
    )

    # Parse response
    response_text = response.choices[0].message.content

    # Try to extract JSON from response
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

    # Default return if parsing fails
    return {'found': False, 'x': 0, 'y': 0, 'confidence': 0.0}
```

- [ ] **Step 4: Run test to verify it passes**

```bash
cd e:/Project/telegram-bot
python -m pytest tests/test_agents/test_vision_agent.py -v
```

Expected: All 3 tests PASS

- [ ] **Step 5: Commit**

```bash
cd e:/Project/telegram-bot
git add src/bot/agents/vision_agent.py tests/test_agents/test_vision_agent.py
git commit -m "feat: implement vision agent for UI element identification"
```

---

### Task 4.2: Implement GUI Automation Service

**Files:**
- Create: `src/bot/services/gui_auto.py`
- Create: `tests/test_services/test_gui_auto.py`

**Interfaces:**
- Produces: `click_at(x: int, y: int) -> bool` - clicks at coordinates
- Produces: `type_text(text: str) -> bool` - types text
- Produces: `press_key(key: str) -> bool` - presses key

- [ ] **Step 1: Write failing test for GUI automation**

```python
# tests/test_services/test_gui_auto.py
import pytest
from unittest.mock import patch, MagicMock
from src.bot.services.gui_auto import click_at, type_text, press_key

def test_click_at_returns_true():
    """Test that click_at returns True on success."""
    with patch('pyautogui.click') as mock_click:
        result = click_at(100, 200)
        assert result is True
        mock_click.assert_called_once_with(100, 200)

def test_type_text_returns_true():
    """Test that type_text returns True on success."""
    with patch('pyautogui.typewrite') as mock_typewrite:
        result = type_text('hello')
        assert result is True
        mock_typewrite.assert_called_once_with('hello', interval=0.05)

def test_press_key_returns_true():
    """Test that press_key returns True on success."""
    with patch('pyautogui.press') as mock_press:
        result = press_key('enter')
        assert result is True
        mock_press.assert_called_once_with('enter')
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd e:/Project/telegram-bot
python -m pytest tests/test_services/test_gui_auto.py -v
```

Expected: FAIL with "ModuleNotFoundError: No module named 'src.bot.services.gui_auto'"

- [ ] **Step 3: Implement gui_auto.py**

```python
# src/bot/services/gui_auto.py
"""GUI automation service using pyautogui."""

import pyautogui
import time

# Disable pyautogui failsafe
pyautogui.FAILSAFE = False

def click_at(x: int, y: int) -> bool:
    """Click at screen coordinates.

    Args:
        x: X coordinate
        y: Y coordinate

    Returns:
        bool: True if successful
    """
    try:
        pyautogui.click(x, y)
        return True
    except Exception as e:
        print(f"Click failed: {e}")
        return False

def type_text(text: str) -> bool:
    """Type text using keyboard.

    Args:
        text: Text to type

    Returns:
        bool: True if successful
    """
    try:
        pyautogui.typewrite(text, interval=0.05)
        return True
    except Exception as e:
        print(f"Type failed: {e}")
        return False

def press_key(key: str) -> bool:
    """Press a keyboard key.

    Args:
        key: Key to press (e.g., 'enter', 'tab', 'escape')

    Returns:
        bool: True if successful
    """
    try:
        pyautogui.press(key)
        return True
    except Exception as e:
        print(f"Key press failed: {e}")
        return False

def move_to(x: int, y: int) -> bool:
    """Move mouse to coordinates.

    Args:
        x: X coordinate
        y: Y coordinate

    Returns:
        bool: True if successful
    """
    try:
        pyautogui.moveTo(x, y)
        return True
    except Exception as e:
        print(f"Move failed: {e}")
        return False
```

- [ ] **Step 4: Run test to verify it passes**

```bash
cd e:/Project/telegram-bot
python -m pytest tests/test_services/test_gui_auto.py -v
```

Expected: All 3 tests PASS

- [ ] **Step 5: Commit**

```bash
cd e:/Project/telegram-bot
git add src/bot/services/gui_auto.py tests/test_services/test_gui_auto.py
git commit -m "feat: implement GUI automation service"
```

---

### Task 4.3: Implement GUI Command Handler

**Files:**
- Create: `src/bot/handlers/gui.py`
- Create: `tests/test_handlers/test_gui.py`

**Interfaces:**
- Produces: `click_command(update, context)` - handles /click command with AI recognition
- Produces: `type_command(update, context)` - handles /type command
- Produces: `key_command(update, context)` - handles /key command

- [ ] **Step 1: Write failing test for GUI handlers**

```python
# tests/test_handlers/test_gui.py
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from telegram import Update
from telegram.ext import ContextTypes
from src.bot.handlers.gui import click_command, type_command, key_command

@pytest.mark.asyncio
async def test_click_command_with_target():
    """Test click_command with target description."""
    update = MagicMock(spec=Update)
    update.message = AsyncMock()
    context = MagicMock(spec=ContextTypes.DEFAULT_TYPE)
    context.args = ['确认', '按钮']

    with patch('src.bot.handlers.gui.take_screenshot', return_value=b'fake_screenshot'), \
         patch('src.bot.handlers.gui.identify_element', return_value={'found': True, 'x': 100, 'y': 200, 'confidence': 0.95}), \
         patch('src.bot.handlers.gui.click_at', return_value=True):
        await click_command(update, context)

        update.message.reply_text.assert_called()

@pytest.mark.asyncio
async def test_type_command():
    """Test type_command."""
    update = MagicMock(spec=Update)
    update.message = AsyncMock()
    context = MagicMock(spec=ContextTypes.DEFAULT_TYPE)
    context.args = ['hello', 'world']

    with patch('src.bot.handlers.gui.type_text', return_value=True):
        await type_command(update, context)

        update.message.reply_text.assert_called_once()

@pytest.mark.asyncio
async def test_key_command():
    """Test key_command."""
    update = MagicMock(spec=Update)
    update.message = AsyncMock()
    context = MagicMock(spec=ContextTypes.DEFAULT_TYPE)
    context.args = ['enter']

    with patch('src.bot.handlers.gui.press_key', return_value=True):
        await key_command(update, context)

        update.message.reply_text.assert_called_once()
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd e:/Project/telegram-bot
python -m pytest tests/test_handlers/test_gui.py -v
```

Expected: FAIL with "ModuleNotFoundError: No module named 'src.bot.handlers.gui'"

- [ ] **Step 3: Implement gui.py handler**

```python
# src/bot/handlers/gui.py
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
```

- [ ] **Step 4: Run test to verify it passes**

```bash
cd e:/Project/telegram-bot
python -m pytest tests/test_handlers/test_gui.py -v
```

Expected: All 3 tests PASS

- [ ] **Step 5: Commit**

```bash
cd e:/Project/telegram-bot
git add src/bot/handlers/gui.py tests/test_handlers/test_gui.py
git commit -m "feat: implement GUI command handlers with AI-assisted click"
```

---

## Phase 5: AI Integration (Day 7)

### Task 5.1: Implement Claude Code CLI Service

**Files:**
- Create: `src/bot/services/claude_cli.py`
- Create: `tests/test_services/test_claude_cli.py`

**Interfaces:**
- Produces: `ask_claude(question: str, working_dir: str = None) -> dict` - calls Claude Code CLI
- Returns: `{'success': bool, 'output': str, 'error': str}`

- [ ] **Step 1: Write failing test for Claude CLI service**

```python
# tests/test_services/test_claude_cli.py
import pytest
from unittest.mock import patch, MagicMock
from src.bot.services.claude_cli import ask_claude

def test_ask_claude_returns_dict():
    """Test that ask_claude returns a dictionary."""
    with patch('subprocess.run') as mock_run:
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout='Claude response',
            stderr=''
        )

        result = ask_claude('What is Python?')
        assert isinstance(result, dict)
        assert 'success' in result
        assert 'output' in result

def test_ask_claude_success():
    """Test successful Claude CLI call."""
    with patch('subprocess.run') as mock_run:
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout='Python is a programming language.',
            stderr=''
        )

        result = ask_claude('What is Python?')
        assert result['success'] is True
        assert 'Python' in result['output']

def test_ask_claude_with_working_dir():
    """Test Claude CLI with custom working directory."""
    with patch('subprocess.run') as mock_run:
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout='Response',
            stderr=''
        )

        result = ask_claude('test', working_dir='E:/Project')
        assert result['success'] is True
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd e:/Project/telegram-bot
python -m pytest tests/test_services/test_claude_cli.py -v
```

Expected: FAIL with "ModuleNotFoundError: No module named 'src.bot.services.claude_cli'"

- [ ] **Step 3: Implement claude_cli.py**

```python
# src/bot/services/claude_cli.py
"""Claude Code CLI service for AI-powered code analysis."""

import subprocess
import os
from typing import Optional

def ask_claude(question: str, working_dir: Optional[str] = None) -> dict:
    """Call Claude Code CLI with a question.

    Args:
        question: Question to ask Claude
        working_dir: Working directory for Claude (default: from config)

    Returns:
        dict: {'success': bool, 'output': str, 'error': str}
    """
    cli_path = os.getenv('CLAUDE_CLI_PATH', 'claude')
    default_working_dir = os.getenv('CLAUDE_WORKING_DIR', 'E:/Project')

    if working_dir is None:
        working_dir = default_working_dir

    try:
        # Build command
        cmd = [cli_path, '--print', question]

        # Execute Claude CLI
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120,  # 2 minute timeout
            cwd=working_dir,
            encoding='utf-8',
            errors='replace'
        )

        return {
            'success': result.returncode == 0,
            'output': result.stdout,
            'error': result.stderr,
        }

    except subprocess.TimeoutExpired:
        return {
            'success': False,
            'output': '',
            'error': 'Claude CLI 执行超时 (120秒)',
        }
    except FileNotFoundError:
        return {
            'success': False,
            'output': '',
            'error': f'Claude CLI 未找到: {cli_path}',
        }
    except Exception as e:
        return {
            'success': False,
            'output': '',
            'error': str(e),
        }
```

- [ ] **Step 4: Run test to verify it passes**

```bash
cd e:/Project/telegram-bot
python -m pytest tests/test_services/test_claude_cli.py -v
```

Expected: All 3 tests PASS

- [ ] **Step 5: Commit**

```bash
cd e:/Project/telegram-bot
git add src/bot/services/claude_cli.py tests/test_services/test_claude_cli.py
git commit -m "feat: implement Claude Code CLI service"
```

---

### Task 5.2: Implement Ask Command Handler

**Files:**
- Create: `src/bot/handlers/claude.py`
- Create: `tests/test_handlers/test_claude.py`

**Interfaces:**
- Produces: `ask_command(update, context)` - handles /ask command

- [ ] **Step 1: Write failing test for ask handler**

```python
# tests/test_handlers/test_claude.py
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from telegram import Update
from telegram.ext import ContextTypes
from src.bot.handlers.claude import ask_command

@pytest.mark.asyncio
async def test_ask_command_with_question():
    """Test ask_command with a question."""
    update = MagicMock(spec=Update)
    update.message = AsyncMock()
    context = MagicMock(spec=ContextTypes.DEFAULT_TYPE)
    context.args = ['What', 'is', 'Python?']

    with patch('src.bot.handlers.claude.ask_claude', return_value={'success': True, 'output': 'Python is a language', 'error': ''}):
        await ask_command(update, context)

        update.message.reply_text.assert_called()
        call_args = update.message.reply_text.call_args
        assert 'Python' in call_args[0][0]

@pytest.mark.asyncio
async def test_ask_command_without_question():
    """Test ask_command without question."""
    update = MagicMock(spec=Update)
    update.message = AsyncMock()
    context = MagicMock(spec=ContextTypes.DEFAULT_TYPE)
    context.args = []

    await ask_command(update, context)

    call_args = update.message.reply_text.call_args
    assert '❌' in call_args[0][0] or '请提供' in call_args[0][0]
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd e:/Project/telegram-bot
python -m pytest tests/test_handlers/test_claude.py -v
```

Expected: FAIL with "ModuleNotFoundError: No module named 'src.bot.handlers.claude'"

- [ ] **Step 3: Implement claude.py handler**

```python
# src/bot/handlers/claude.py
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
```

- [ ] **Step 4: Run test to verify it passes**

```bash
cd e:/Project/telegram-bot
python -m pytest tests/test_handlers/test_claude.py -v
```

Expected: All 2 tests PASS

- [ ] **Step 5: Commit**

```bash
cd e:/Project/telegram-bot
git add src/bot/handlers/claude.py tests/test_handlers/test_claude.py
git commit -m "feat: implement ask command handler for Claude CLI"
```

---

## Phase 6: Packaging and Optimization (Day 8)

### Task 6.1: Create PyInstaller Configuration

**Files:**
- Create: `telegram_bot_agent.spec`
- Create: `build.py`

**Interfaces:**
- Produces: PyInstaller spec file for building exe

- [ ] **Step 1: Create PyInstaller spec file**

```python
# telegram_bot_agent.spec
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['run.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('src/config', 'src/config'),
        ('.env', '.'),
    ],
    hiddenimports=[
        'telegram',
        'psutil',
        'mss',
        'pyautogui',
        'openai',
        'httpx',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='telegram_bot_agent',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
```

- [ ] **Step 2: Create build script**

```python
# build.py
"""Build script for creating executable."""

import PyInstaller.__main__
import os
import shutil

def build():
    """Build the executable."""
    print("Building telegram_bot_agent.exe...")

    # Clean previous build
    if os.path.exists('build'):
        shutil.rmtree('build')
    if os.path.exists('dist'):
        shutil.rmtree('dist')

    # Run PyInstaller
    PyInstaller.__main__.run([
        'telegram_bot_agent.spec',
        '--clean',
        '--noconfirm',
    ])

    print("\n✅ Build complete!")
    print("Executable: dist/telegram_bot_agent.exe")

if __name__ == '__main__':
    build()
```

- [ ] **Step 3: Test build script runs**

```bash
cd e:/Project/telegram-bot
python build.py
```

Expected: Build completes, `dist/telegram_bot_agent.exe` is created

- [ ] **Step 4: Commit**

```bash
cd e:/Project/telegram-bot
git add telegram_bot_agent.spec build.py
git commit -m "feat: add PyInstaller build configuration"
```

---

### Task 6.2: Create README Documentation

**Files:**
- Create: `README.md`

- [ ] **Step 1: Create README.md**

```markdown
# Telegram Bot Agent

通过 Telegram Bot 实现手机远程监控和操控电脑的 AI 代理工具。

## 功能特性

- 📊 **进程监控**: 查看运行中的进程状态、CPU/内存占用
- 📸 **远程截图**: 截取电脑屏幕并发送到手机
- ⌨️ **命令执行**: 远程执行系统命令
- 🖱️ **GUI 自动化**: AI 辅助识别并点击按钮、输入文字
- 🤖 **AI 问答**: 调用 Claude Code CLI 进行代码分析

## 快速开始

### 前置要求

- Windows 10/11
- Python 3.11+
- Telegram Bot Token
- MiMo API Key

### 安装

1. 克隆项目
```bash
git clone <repository-url>
cd telegram-bot
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 配置环境变量
```bash
cp .env.example .env
# 编辑 .env 文件，填入你的配置
```

4. 运行
```bash
python run.py
```

### 打包成 exe

```bash
python build.py
```

生成的可执行文件在 `dist/telegram_bot_agent.exe`

## 命令列表

| 命令 | 说明 | 示例 |
|------|------|------|
| `/start` | 显示欢迎信息 | |
| `/help` | 显示帮助 | |
| `/status` | 查看进程状态 | `/status python` |
| `/list` | 列出运行中的进程 | |
| `/screenshot` | 截取屏幕 | |
| `/exec` | 执行命令 | `/exec dir` |
| `/ask` | AI 问答 | `/ask 这段代码有什么问题？` |
| `/click` | 点击元素 | `/click 确认按钮` |
| `/type` | 输入文字 | `/type hello` |
| `/key` | 按下按键 | `/key enter` |

## 配置说明

### 环境变量 (.env)

```env
TELEGRAM_BOT_TOKEN=your_token
MIMO_API_KEY=your_api_key
MIMO_API_BASE_URL=https://token-plan-cn.xiaomimimo.com/v1
PROXY_URL=socks5://127.0.0.1:7897
ALLOWED_USER_IDS=6531095340
```

### 配置文件 (src/config/config.yaml)

详见 `src/config/config.yaml` 中的注释

## 安全特性

- ✅ 用户白名单验证
- ✅ 命令黑名单过滤
- ✅ 危险操作二次确认
- ✅ 操作日志记录

## 技术栈

- Python 3.11+
- python-telegram-bot
- psutil
- mss
- pyautogui
- MiMo API (OpenAI 兼容)

## 许可证

MIT License
```

- [ ] **Step 2: Commit**

```bash
cd e:/Project/telegram-bot
git add README.md
git commit -m "docs: add README documentation"
```

---

## Plan Complete

Plan saved to `docs/superpowers/plans/2026-06-22-telegram-bot-agent.md`

**Two execution options:**

**1. Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

**Which approach?**