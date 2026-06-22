"""Process monitoring service using psutil."""

import psutil
import time
from typing import Optional

# Processes to exclude from monitoring
EXCLUDED_PROCESSES = [
    'System Idle Process',
    'System',
    'Registry',
]

def get_process_list() -> list[dict]:
    """Get list of all running processes.

    Returns:
        list: List of process dictionaries with name, pid, cpu, memory
    """
    # First call to initialize CPU percent tracking
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        try:
            proc.cpu_percent()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    # Wait a bit for CPU percent to be calculated
    time.sleep(0.2)

    # Second call to get actual CPU percent
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            pinfo = proc.info
            name = pinfo['name']

            # Skip excluded processes
            if name in EXCLUDED_PROCESSES:
                continue

            cpu = pinfo['cpu_percent'] or 0.0
            memory = pinfo['memory_percent'] or 0.0

            # Cap CPU at 100% (in case of calculation errors)
            cpu = min(cpu, 100.0)

            processes.append({
                'name': name,
                'pid': pinfo['pid'],
                'cpu': round(cpu, 1),
                'memory': round(memory, 1),
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    # Sort by CPU usage (descending)
    processes.sort(key=lambda p: p['cpu'], reverse=True)
    return processes

def get_process_status(process_name: str) -> Optional[dict]:
    """Get status of a specific process by name.

    Args:
        process_name: Name of the process to find

    Returns:
        dict or None: Process status dictionary or None if not found
    """
    # First call to initialize CPU percent tracking
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        try:
            proc.cpu_percent()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    # Wait a bit for CPU percent to be calculated
    time.sleep(0.2)

    # Second call to get actual CPU percent
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status']):
        try:
            if proc.info['name'].lower() == process_name.lower():
                cpu = proc.info['cpu_percent'] or 0.0
                memory = proc.info['memory_percent'] or 0.0

                # Cap CPU at 100%
                cpu = min(cpu, 100.0)

                return {
                    'name': proc.info['name'],
                    'pid': proc.info['pid'],
                    'cpu': round(cpu, 1),
                    'memory': round(memory, 1),
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