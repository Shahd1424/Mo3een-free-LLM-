import logging
import uuid


def get_logger(name: str):
    """
    Returns a configured logger instance used across Mo3een services.
    Ensures no duplicate handlers and keeps logs simple & clean.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Avoid adding multiple handlers when reloading with uvicorn
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


def generate_request_id() -> str:
    """
    Generates a unique request ID used for tracking requests & errors
    across the explanation and evaluation pipeline.
    """
    return str(uuid.uuid4())
