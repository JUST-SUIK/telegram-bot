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