"""Command execution service."""

import subprocess

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