import pytest
from piedmont.config import Config
from piedmont.logger import logger


def test_load_config():
    config = Config('tests/config.yaml')
    assert config is not None
    assert 'name' in config.bridge_conf.keys()
    logger.debug('Test debug message111')
    logger.info('Test info message.')
