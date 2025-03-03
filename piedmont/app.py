from __future__ import annotations

import typing as t
import functools


from .bridge import BridgeClient
from .serials import SerialClient
from .typing import T_PP_Message_Payload
from .config import PiedmontConfig
from .logger import logger


class Piedmont(PiedmontConfig):

    bridge_client: BridgeClient
    serial_client: SerialClient

    def __init__(
            self, conf_path: str = 'config.yaml',
    ) -> None:
        super().__init__(conf_path)
        self.bridge_client = BridgeClient(self.bridge_conf)
        self.serial_client = SerialClient(self.serial_conf)

    def bridge(self, messageId: str, **options: t.Any):
        def decorator(func):
            self.bridge_client.regist_bridge_handler(messageId.upper(), func)

            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper
        return decorator

    def serial(self, messageId: str, **options: t.Any):
        def decorator(func):
            self.serial_client.regist_serial_handler(messageId.upper(), func)

            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper
        return decorator

    def send_pp_connection(self, messageId: str, value: T_PP_Message_Payload):
        self.bridge_client.send(messageId.upper(), value)

    def send_serial(self):
        pass
