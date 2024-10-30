from loguru import logger
import sys
import os

def setup_logger():
    log_directory = "logging"
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    logger.remove()
    
    logger.add(
        f"{log_directory}/app.log",
        rotation="10 MB",
        level="INFO",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {module}:{function}:{line} | {message}"
    )
    
    logger.add(
        sys.stderr,
        level="INFO",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
    )

    return logger

logger = setup_logger()
