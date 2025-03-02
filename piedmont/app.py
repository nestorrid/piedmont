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

    # def connect_serial(
    #     self,
    #     config: T_Serial_Config = None,
    #     auto_start_listen=True
    # ):
    #     try:
    #         if isinstance(config, serial.Serial):
    #             self.serial_client = config
    #         elif isinstance(config, t.List):
    #             self.serial_client = serial.Serial(*config)
    #         elif isinstance(config, t.Dict):
    #             self.serial_client = serial.Serial(**config)
    #         else:
    #             if not self.port or not self.baudrate:
    #                 raise ValueError(
    #                     f'You must specify `port` and `baudrate` with initialization or provide a valid serial configuration before connect.')
    #             self.serial_client = serial.Serial(
    #                 self.port, self.baudrate, self.serial_timeout)

    #         self.logger.info(
    #             f'Serial connected to port: {self.serial_client.port}, baudrate: {self.baudrate}')

    #         if auto_start_listen:
    #             self._read_serial()

    #     except serial.SerialException as e:
    #         self.logger.error(f'Serial connection error: {e}')

    # def _read_serial(self):
    #     data = self.serial_client.readline().decode('utf-8').strip()
    #     self.logger.info(f'Received data from serial: `{data}`.')

    # def __del__(self):
        # if self.serial_client.is_open:
        #     self.serial_client.close()
        #     self.logger.info('Serial connection closed.')
