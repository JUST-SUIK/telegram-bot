"""Vision agent for UI element identification using MiMo API."""

import os
import base64
import json
import logging
from openai import OpenAI
from typing import Optional

logger = logging.getLogger(__name__)

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
        logger.error(f"Vision agent error: {e}")
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