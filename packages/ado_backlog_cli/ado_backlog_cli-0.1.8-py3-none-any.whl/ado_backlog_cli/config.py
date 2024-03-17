import os
import re
import yaml
import logging
from typing import Dict

logger = logging.getLogger(__name__)

def ensure_config_path() -> str:
    """
    Ensures the configuration directory and file exist, creating them if they do not.

    Returns:
        str: The path to the configuration file.
    """
    config_dir = os.path.expanduser('~/.config/ado-backlog-cli')
    config_path = os.path.join(config_dir, 'config.yml')

    if not os.path.exists(config_dir):
        os.makedirs(config_dir)

    if not os.path.isfile(config_path):
        with open(config_path, 'w') as file:
            yaml.dump({}, file)

    return config_path

def is_valid_url(url: str) -> bool:
    """
    Validates a URL using a simple regex.

    Args:
        url (str): The URL to validate.

    Returns:
        bool: True if the URL is valid, False otherwise.
    """
    return re.match(r'https?://[^\s]+', url) is not None

def load_config() -> Dict:
    """
    Loads and validates the configuration from a YAML file, ensuring required fields are present
    and correct, and handles backslashes in iteration_path.

    Returns:
        Dict: The configuration dictionary with validated and processed fields.
    
    Raises:
        FileNotFoundError: If the configuration file does not exist.
        ValueError: If required fields are missing or invalid.
    """
    config_path = ensure_config_path()

    with open(config_path, 'r') as file:
        config = yaml.safe_load(file) or {}

    required_keys = ['org_url', 'project_name', 'iteration_path']
    missing_keys = [
        key for key in required_keys
        if key not in config.get('azure_devops', {})
    ]

    if missing_keys:
        raise ValueError(f"Missing keys in 'azure_devops': {', '.join(missing_keys)}. "
                         f"Check the configuration at {config_path}.")

    azure_devops = config['azure_devops']

    if not is_valid_url(azure_devops['org_url']):
        raise ValueError(f"Invalid 'org_url': {azure_devops['org_url']}.")

    if not isinstance(azure_devops['project_name'], str):
        raise ValueError("'project_name' must be a string.")

    iteration_path = azure_devops['iteration_path'].replace('\\', '\\\\')
    azure_devops['iteration_path'] = iteration_path

    return config
