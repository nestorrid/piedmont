from piedmont.config import Config


def test_default_config():
    config = Config()
    assert config is not None
    assert 'APP_NAME' in config.keys()
    assert config.port == '9981'


def test_yaml_config():
    config = Config('tests/config.yaml')
    assert config is not None
    assert 'APP_NAME' in config.keys()
    assert config.port == '9981'


def test_create_with_value():
    config = Config('test')
