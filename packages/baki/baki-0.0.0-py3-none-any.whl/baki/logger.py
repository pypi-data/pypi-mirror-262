"""
Logging functionality
"""

import logging
import os

from baki.config import get_cache_dirpath, get_config_name


class ColoredFormatter(logging.Formatter):
    """
    A custom formatter for adding colors to log messages.
    """

    COLORS = {
        "RESET": "\033[0m",
        "DEBUG": "\033[0;36m",  # Cyan
        "INFO": "\033[0;32m",  # Green
        "WARNING": "\033[0;33m",  # Yellow
        "ERROR": "\033[0;31m",  # Red
        "CRITICAL": "\033[1;31m",  # Bold Red
    }

    def format(self, record):
        """
        Overrides the format method to add color codes to the log messages.

        Args:
            record (LogRecord): The log record to be formatted.

        Returns:
            str: The formatted log message with color codes.
        """
        log_level = record.levelname
        record.color = self.COLORS[log_level]
        record.reset = self.COLORS["RESET"]
        return super().format(record)


class Logger(logging.Logger):
    """
    Custom logger class.
    """

    def __init__(self, level=logging.NOTSET):
        """
        Initializes the Logger class with console and file handlers.

        Args:
            level (int): The logging level for the logger.
        """
        super().__init__(__name__, level)

        log_filepath = os.path.join(get_cache_dirpath(),
                                    f"{get_config_name()}.log")

        if not self.handlers:
            # Create handlers
            c_handler = logging.StreamHandler()
            f_handler = logging.FileHandler(log_filepath)

            c_handler.setLevel(level)
            f_handler.setLevel(logging.WARNING)

            # Create formatters and add them to handlers
            c_format = ColoredFormatter("[%(color)s%(levelname)-8s%(reset)s]: \
                %(message)s - %(filename)s:%(lineno)d")
            f_format = logging.Formatter(
                "[%(levelname)-8s]: %(asctime)s - \
                %(message)s - %(filename)s:%(lineno)d",
                datefmt="%Y-%m-%d %H:%M:%S",
            )

            c_handler.setFormatter(c_format)
            f_handler.setFormatter(f_format)

            # Add handlers to the logger
            self.addHandler(c_handler)
            self.addHandler(f_handler)
