import logging
import sys

sys.path.append("..")


def setup_logger(name: str) -> logging.Logger:
    """
    Set up a logger with the specified name and a specific format.

    Args:
        name (str): The name of the logger.

    Returns:
        logging.Logger: Configured logger instance.
    """
    # Create a custom logger
    logger = logging.getLogger(name)

    # Set the default logging level to DEBUG
    logger.setLevel(logging.DEBUG)

    # Create handlers
    console_handler = logging.StreamHandler()

    # Create formatters and add them to the handlers
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(console_handler)

    return logger
