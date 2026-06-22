"""GUI automation service using pyautogui."""

try:
    import pyautogui
    # Disable pyautogui failsafe
    pyautogui.FAILSAFE = False
except ImportError:
    pyautogui = None
    print("Warning: pyautogui not installed. GUI automation features will be disabled.")

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