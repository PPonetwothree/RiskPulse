import logging
import sys


def setup_logger(name='riskpulse', level=logging.INFO):
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter(
            '[%(asctime)s] %(levelname)-8s %(name)-20s %(message)s',
            datefmt='%H:%M:%S'
        ))
        logger.addHandler(handler)
    logger.setLevel(level)
    return logger
