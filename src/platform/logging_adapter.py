import logging
from logging import Logger

def setup_logging(log_level: int = logging.INFO) -> Logger:
    logger = logging.getLogger("rebuild")
    logger.setLevel(log_level)
    if not logger.handlers:
        ch = logging.StreamHandler()
        ch.setLevel(log_level)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    return logger
