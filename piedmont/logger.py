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
            'format': "[Piedmont][%(levelname)s]:\t%(message)s"
        },
        'detailed': {
            'format': "$ %(asctime)s [%(name)s][%(levelname)s][%(threadName)s:%(process)d]::%(module)s::\t%(message)s"
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
            'level': 'DEBUG',
            'filename': 'piedmont.log',
            'formatter': 'detailed',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5
        }
    },
    'loggers': {
        'piedmont': {
            'level': 'ERROR',
            'handlers': ['file'],
            'propagate': False
        },
        'piedmont-console': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False
        }
    }
}


logging.config.dictConfig(LOGGING_CONFIG)

logger = logging.getLogger('piedmont')
console = logging.getLogger('piedmont-console')


def info(msg: object, *args, **kwargs):
    logger.info(msg, *args, **kwargs)
    console.info(msg, *args, **kwargs)


def debug(msg: object, *args, **kwargs):
    logger.debug(msg, *args, **kwargs)
    console.debug(msg, *args, **kwargs)


def warning(msg: object, *args, **kwargs):
    logger.warning(msg, *args, **kwargs)
    console.warning(msg, *args, **kwargs)


def error(msg: object, *args, **kwargs):
    logger.error(msg, *args, **kwargs)
    console.error(msg, *args, **kwargs)


def critical(msg: object, *args, **kwargs):
    logger.critical(msg, *args, **kwargs)
    console.critical(msg, *args, **kwargs)


def set_dev_mode(flag=True):
    if flag:
        logger.setLevel(logging.DEBUG)
        console.setLevel(logging.DEBUG)
        console.debug('Set log level to: `DEBUG`.')
        logger.debug(
            f'\n{"=" * 48}\n{">"*15} PIEDMONT DEV LOG {"<"*15}\n{"=" * 48}'
        )
    else:
        logger.setLevel(logging.CRITICAL)
        console.setLevel(logging.INFO)
