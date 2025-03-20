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
        'current': {
            'class': 'logging.FileHandler',
            'level': 'DEBUG',
            'formatter': 'detailed',
            'filename': 'piedmont.log',
            'mode': 'w'
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'INFO',
            'formatter': 'detailed',
            'filename': 'piedmont.rotating.log',
            'maxBytes': 10485760,
            'backupCount': 5
        },
        'error_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'ERROR',
            'formatter': 'detailed',
            'filename': 'piedmont.error.log',
            'maxBytes': 10485760,
            'backupCount': 5
        }
    },
    'loggers': {
        'piedmont-dev': {
            'level': 'DEBUG',
            'handlers': ['console', 'current', 'file', 'error_file'],
            'propagate': False
        },
        'piedmont': {
            'level': 'INFO',
            'handlers': ['console', 'error_file'],
            'propagate': False
        }
    }
}

logging.config.dictConfig(LOGGING_CONFIG)

devlogger = logging.getLogger('piedmont-dev')
logger = logging.getLogger('piedmont')

devlogger.debug(
    f'\n{"=" * 51}\n{">"*20} LOG START {"<"*20}\n{"=" * 51}')
