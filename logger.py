import logging
import os

def setup_logger():
    """
    Set up and return a logger for the application.
    """

    # Define the log file name
    log_file = "log.txt"

    # Create the logger
    logger = logging.getLogger('FoolsGoldPyWriter')
    logger.setLevel(logging.INFO)

    # Create a file handler for the log file in append mode
    file_handler = logging.FileHandler(log_file, mode='a')
    file_handler.setLevel(logging.INFO)

    # Create a formatter for the log messages
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Add the file handler to the logger
    logger.addHandler(file_handler)

    return logger
