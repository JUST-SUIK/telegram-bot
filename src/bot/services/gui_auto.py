"""GUI automation service using pyautogui."""

try:
    import pyautogui
    # Keep FAILSAFE enabled for safety - move mouse to corner to abort
    pyautogui.FAILSAFE = True
    # Set a small pause between actions for stability
    pyautogui.PAUSE = 0.1
except ImportError:
    pyautogui = None
    import logging
    logging.warning("pyautogui not installed. GUI automation features will be disabled.")

import logging

logger = logging.getLogger(__name__)

def click_at(x: int, y: int) -> bool:
    """Click at screen coordinates.

    Args:
        x: X coordinate
        y: Y coordinate

    Returns:
        bool: True if successful
    """
    if pyautogui is None:
        logger.error("pyautogui not installed")
        return False
    try:
        pyautogui.click(x, y)
        return True
    except Exception as e:
        logger.error(f"Click failed at ({x}, {y}): {e}")
        return False

def type_text(text: str) -> bool:
    """Type text using keyboard.

    Args:
        text: Text to type

    Returns:
        bool: True if successful
    """
    if pyautogui is None:
        logger.error("pyautogui not installed")
        return False
    try:
        # Use write() for better Unicode support
        pyautogui.write(text, interval=0.05)
        return True
    except Exception as e:
        logger.error(f"Type failed: {e}")
        return False

def press_key(key: str) -> bool:
    """Press a keyboard key.

    Args:
        key: Key to press (e.g., 'enter', 'tab', 'escape')

    Returns:
        bool: True if successful
    """
    if pyautogui is None:
        logger.error("pyautogui not installed")
        return False
    try:
        pyautogui.press(key)
        return True
    except Exception as e:
        logger.error(f"Key press failed for '{key}': {e}")
        return False

def move_to(x: int, y: int) -> bool:
    """Move mouse to coordinates.

    Args:
        x: X coordinate
        y: Y coordinate

    Returns:
        bool: True if successful
    """
    if pyautogui is None:
        logger.error("pyautogui not installed")
        return False
    try:
        pyautogui.moveTo(x, y)
        return True
    except Exception as e:
        logger.error(f"Move failed to ({x}, {y}): {e}")
        return False