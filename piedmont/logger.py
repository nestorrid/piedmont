import logging
import logging.config
import logging.handlers
import typing as t
import sys


LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': "$ %(asctime)s [%(name)s][%(levelname)s]:\n> %(message)s"
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'simple',
            'stream': sys.stdout
        },
    },
    'loggers': {
        'piedmont': {
            'level': 'INFO',
            'handlers': ['console'],
            'propagate': False
        }
    }
}

logging.config.dictConfig(LOGGING_CONFIG)

logger = logging.getLogger('piedmont')


def info(msg: object, *args, **kwargs):
    logger.info(msg, *args, **kwargs)


def debug(msg: object, *args, **kwargs):
    logger.debug(msg, *args, **kwargs)


def warning(msg: object, *args, **kwargs):
    logger.warning(msg, *args, **kwargs)


def error(msg: object, *args, **kwargs):
    logger.error(msg, *args, **kwargs)


def critical(msg: object, *args, **kwargs):
    logger.critical(msg, *args, **kwargs)


def _create_dev_logger():
    l = logging.getLogger('piedmont-dev')
    l.setLevel(logging.DEBUG)
    h1 = logging.handlers.RotatingFileHandler('piedmont.log')
    h1.setLevel(logging.DEBUG)
    h2 = logging.StreamHandler(sys.stdout)
    h1.setLevel(logging.DEBUG)
    fmt_s = logging.Formatter(
        "$ %(asctime)s [%(name)s][%(levelname)s]:\n> %(message)s")
    fmt_d = logging.Formatter(
        "$ %(asctime)s [%(name)s][%(levelname)s][%(threadName)s:%(process)d]::%(module)s::\n> %(message)s")
    h1.setFormatter(fmt_d)
    h2.setFormatter(fmt_s)
    l.addHandler(h1)
    l.addHandler(h2)

    return l


_dev_logger: logging.Logger = None


def devlog(msg: object, level=logging.DEBUG, *args, **kwargs):
    if _dev_logger:
        _dev_logger.log(level, msg, *args, **kwargs)


def set_dev_mode(flag=True):
    global _dev_logger
    if flag:
        _dev_logger = _create_dev_logger()
        devlog(f'\n{"=" * 48}\n{">"*15} PIEDMONT DEV LOG {"<"*15}\n{"=" * 48}')
    else:
        logging.getLogger('piedmont-dev').setLevel(logging.CRITICAL)
