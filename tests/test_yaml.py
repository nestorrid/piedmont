import pytest
from piedmont.config import PiedmontConfig
from piedmont.logger import logger


def test_load_config():
    config = PiedmontConfig('tests/config.yaml')
    assert config is not None
    assert 'name' in config.bridge_conf.keys()
    logger.debug('Test debug message111')
    logger.info('Test info message.')
