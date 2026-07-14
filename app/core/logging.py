import logging
import sys

from app.core.config import settings


def get_logger(name: str | None = None) -> logging.Logger:
    logger = logging.getLogger(name or "localhub")
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter("[%(asctime)s] %(levelname)s %(name)s: %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    level_name = (settings.LOG_LEVEL or "INFO").upper()
    logger.setLevel(getattr(logging, level_name, logging.INFO))
    logger.propagate = False
    return logger
