"""
Support for configuration operations.
"""

import os

from xdg_base_dirs import xdg_cache_home, xdg_config_home


def get_config_name():
    """
    Get the configuration name.

    Returns:
        str: The configuration name derived from the module name.
    """
    config_name = __package__
    return config_name


def get_config_dirpath():
    """
    Get the directory path for configuration files based on XDG configuration
    home.

    Returns:
        str: The absolute path to the configuration directory.
    """
    config_dirpath = os.path.join(xdg_config_home(), get_config_name())

    return config_dirpath


def get_cache_dirpath():
    """
    Get the directory path for cache files based on XDG cache home.

    Returns:
        str: The absolute path to the cache directory.
    """
    cache_dirpath = os.path.join(xdg_cache_home(), get_config_name())

    return cache_dirpath


class Config:
    """
    Class for handling configuration operations.
    """

    def __init__(self):
        """
        Initialize the Config class, ensuring the required directories exist.
        """
        dirpaths = (get_config_dirpath(), get_cache_dirpath())

        # Ensure the directory exists, create if not
        for dirpath in dirpaths:
            os.makedirs(dirpath, exist_ok=True)

    def read(self):
        """
        Abstract method for reading the configuration.

        Raises:
            NotImplementedError: This method is not implemented.
        """
        raise NotImplementedError

    def write(self):
        """
        Abstract method for writing the configuration.

        Raises:
            NotImplementedError: This method is not implemented.
        """
        raise NotImplementedError
