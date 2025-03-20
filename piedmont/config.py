from __future__ import annotations

import typing as t
from pathlib import Path

import yaml

from .logger import logger, devlogger


class BaseConfig(dict):

    @property
    def app_name(self) -> str:
        return self['APP_NAME']

    @app_name.setter
    def app_name(self, value):
        self['APP_NAME'] = value

    @property
    def host(self):
        return self['HOST']

    @host.setter
    def host(self, value):
        self['HOST'] = str(value)

    @property
    def port(self):
        return self['PORT']

    @port.setter
    def port(self, value):
        self['PORT'] = str(value)


class FileConfig(BaseConfig):

    def __init__(self, path: Path):
        super().__init__()
        try:
            with open(path, 'r', encoding='utf-8') as f:
                temp = yaml.safe_load(f)
                devlogger.debug(f'load config from file: {temp}')
                self.app_name = temp['name']
                self.host = temp['host']
                self.port = temp['port']
        except Exception as e:
            logger.warning(
                f'Exception occurred while parsing config file: {e}.\n'
                'Using default settings instead.'
            )
            self.update({
                "APP_NAME": 'BridgeApp',
                'HOST': 'http://localhost',
                'PORT': '9981'
            })


class Config(BaseConfig):

    def __init__(
        self,
        name: str = None,
        host: str = None,
        port: str = None,
    ):
        super().__init__()
        self.app_name = name or 'Bridge App'
        self.host = host or 'http://localhost'
        self.port = port or '9981'
