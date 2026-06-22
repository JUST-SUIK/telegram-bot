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