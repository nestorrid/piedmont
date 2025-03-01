import logging


def create_console_logger(name: str):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    fmt = logging.Formatter(
        '> %(asctime)s [%(name)s][%(levelname)s]:\n\t%(message)s')
    console_handler.setFormatter(fmt)
    logger.addHandler(console_handler)
    return logger
