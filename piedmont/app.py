from __future__ import annotations

import typing as t
import functools


from .bridge import BridgeClient
from .config import Config
from .logger import devlogger


class Piedmont():

    _bridge_client: BridgeClient

    def __init__(
            self, config: Config = None
    ) -> None:
        super().__init__()
        self._bridge_client = BridgeClient(config)

    def bridge(self, messageId: str, **options: t.Any):
        def decorator(func):
            self._bridge_client.regist_bridge_handler(messageId.upper(), func)

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

    def send(self, messageId: str, value: T_PP_Message_Payload = "", uppercase=True):
        if uppercase:
            messageId = messageId.upper()

        self._bridge_client.send(messageId, value)
