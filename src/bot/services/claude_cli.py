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