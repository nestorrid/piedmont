import logging
import typing as t


def default_logger():
    logger = logging.getLogger("Piedmont")
    # logger.setLevel(logging.INFO)
    # console_handler = logging.StreamHandler()
    # fmt = logging.Formatter(
    #     '> %(asctime)s [%(name)s][%(levelname)s]:\n\t%(message)s')
    # console_handler.setFormatter(fmt)
    # logger.addHandler(console_handler)
    return logger


logger = default_logger()


def setup_handler(config: t.Dict, handler: logging.Handler):
    if config.get('level'):
        handler.setLevel(config.get('level'))
    fmt = logging.Formatter(config['format'])
    handler.setFormatter(fmt)
    logger.addHandler(handler)


def setup_console_handler(config: t.Dict):
    setup_handler(config, logging.StreamHandler())


def setup_file_handler(config: t.Dict):
    setup_handler(config, logging.FileHandler(config['name'], mode='a'))
    logger.debug(
        f'\n{"=" * 41}\n{">"*15} LOG START {"<"*15}\n{"=" * 41}')


def create_logger(config: t.Dict):
    logger = logging.getLogger('Piedmont')
    logger.setLevel(config.get('level', 'DEBUG'))
    if 'console' in config.keys():
        setup_console_handler(config['console'])
    if 'file' in config.keys():
        setup_file_handler(config['file'])
