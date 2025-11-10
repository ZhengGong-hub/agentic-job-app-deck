"""Rich logging setup."""
from rich.console import Console
from rich.logging import RichHandler
import logging


def setup_logger(name: str = "cv-agentic") -> logging.Logger:
    """
    Setup Rich logger.
    
    Args:
        name: Logger name
        
    Returns:
        Configured logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    if not logger.handlers:
        handler = RichHandler(rich_tracebacks=True)
        handler.setFormatter(logging.Formatter("%(message)s", datefmt="[%X]"))
        logger.addHandler(handler)
    
    return logger

