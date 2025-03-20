import logging
import logging.config
import typing as t
import sys

# 定义日志配置字典
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': "$ %(asctime)s [%(name)s][%(levelname)s]:\n> %(message)s"
        },
        'detailed': {
            'format': "$ %(asctime)s [%(name)s][%(levelname)s][%(threadName)s:%(process)d]::%(module)s::\n> %(message)s"
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'simple',
            'stream': sys.stdout
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'INFO',
            'formatter': 'detailed',
            'filename': 'piedmont.log',
            'maxBytes': 10485760,
            'backupCount': 5
        },
    },
    'loggers': {
        'piedmont-dev': {
            'level': 'CRITICAL',
            'handlers': ['console', 'file'],
            'propagate': False
        },
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


def devlog(msg: object, level=logging.DEBUG, *args, **kwargs):
    logging.getLogger('piedmont-dev').log(level, msg, *args, **kwargs)


def set_dev_mode(flag=True):
    if flag:
        logging.getLogger('piedmont-dev').setLevel(logging.DEBUG)
        devlog(f'\n{"=" * 48}\n{">"*15} PIEDMONT DEV LOG {"<"*15}\n{"=" * 48}')
    else:
        logging.getLogger('piedmont-dev').setLevel(logging.CRITICAL)
