from __future__ import annotations

import yaml
import typing as t
from enum import StrEnum

from .logger import logger, create_logger


class ConfigKey(StrEnum):
    BRIDGE = 'bridge'
    LOGGING = 'logging'
    SERIAL = 'serial'
    OPTIONS = 'options'


class PiedmontConfig:

    config: t.Dict

    def __init__(self, path: t.AnyStr):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                self.config = yaml.safe_load(f)
                create_logger(self.logging_conf)
        except FileNotFoundError as e:
            logger.error(f'Config file: `{path}` does not exist.')
            exit(1)
        except yaml.YAMLError as e:
            logger.error(f'Config file parse error: `{e}`.')
            exit(1)

    @property
    def bridge_conf(self) -> t.Dict:
        return self.config.get(ConfigKey.BRIDGE, None)

    @property
    def serial_conf(self) -> t.Dict:
        return self.config.get(ConfigKey.SERIAL, None)

    @property
    def logging_conf(self) -> t.Dict:
        return self.config.get(ConfigKey.LOGGING, None)

    @property
    def options_conf(self) -> t.Dict:
        return self.config.get(ConfigKey.OPTIONS, None)
