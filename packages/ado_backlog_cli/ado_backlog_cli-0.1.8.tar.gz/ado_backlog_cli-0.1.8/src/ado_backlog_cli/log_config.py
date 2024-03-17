"""
Custom Logging Configuration Module.

This module defines custom log levels for developer and performance tracing messages and
provides a function to set up the default logging configuration with these custom or standard log levels.
"""

import logging

# Custom log level for detailed debug information useful for developers
DEV_LEVEL_NUM: int = 15

# Custom log level for performance tracing
PERF_LEVEL_NUM: int = 25

def setup_custom_log_levels() -> None:
    """
    Adds custom logging levels for developer and performance logs to the logging module.
    
    This function defines 'DEV' and 'PERF' as custom log levels with their respective numeric values.
    It also extends the logging.Logger class with `.dev` and `.perf` methods for logging at these levels.
    """
    # Define a method for logging at the developer level
    def dev(self: logging.Logger, message: str, *args, **kwargs) -> None:
        """
        Logs a 'DEV' level message.
        
        This method is dynamically added to the logging.Logger class and enables logging messages at the DEV level.
        
        Args:
            message (str): The log message.
            *args: Variable length argument list for the log message.
            **kwargs: Arbitrary keyword arguments.
        """
        if self.isEnabledFor(DEV_LEVEL_NUM):
            self._log(DEV_LEVEL_NUM, message, args, **kwargs)

    # Add developer level logging method to the Logger class
    logging.addLevelName(DEV_LEVEL_NUM, "DEV")
    logging.Logger.dev = dev

    # Define a method for logging at the performance level
    def perf(self: logging.Logger, message: str, *args, **kwargs) -> None:
        """
        Logs a 'PERF' level message.
        
        This method is dynamically added to the logging.Logger class and enables logging messages at the PERF level.
        
        Args:
            message (str): The log message.
            *args: Variable length argument list for the log message.
            **kwargs: Arbitrary keyword arguments.
        """
        if self.isEnabledFor(PERF_LEVEL_NUM):
            self._log(PERF_LEVEL_NUM, message, args, **kwargs)

    # Add performance level logging method to the Logger class
    logging.addLevelName(PERF_LEVEL_NUM, "PERF")
    logging.Logger.perf = perf

def setup_logging(log_level: str = 'INFO') -> None:
    """
    Configures the root logger with the specified log level and a standard log format.
    
    This function sets up the logging system with custom log levels if specified, or
    falls back to standard log levels otherwise. It raises a ValueError if an invalid log level is provided.
    
    Args:
        log_level (str): The log level to configure the root logger with. Defaults to 'INFO'.
        
    Raises:
        ValueError: If `log_level` is not a valid custom or standard log level.
    """
    # Initialize custom log levels
    setup_custom_log_levels()
    print(f"Custom log levels initialized with log level: {log_level}")

    # Map log level string to its numeric value, including custom levels
    if log_level.upper() == "DEV":
        numeric_level = DEV_LEVEL_NUM
    elif log_level.upper() == "PERF":
        numeric_level = PERF_LEVEL_NUM
    else:
        # Attempt to convert standard log level names to their numeric values
        numeric_level = getattr(logging, log_level.upper(), None)
        if not isinstance(numeric_level, int):
            raise ValueError(f'Invalid log level: {log_level}')

    # Configure basic logging settings with the determined log level
    logging.basicConfig(level=numeric_level, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')
