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