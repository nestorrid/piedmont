from __future__ import annotations

import typing as t
import json
import functools
import logging
import serial
import asyncio
# import serial_asyncio
# import socketio

from .logger import create_console_logger
from .bridge import BridgeClient
from .serials import SerialClient
from .api import ApiClient
from .typing import T_PP_Message_Payload


class Piedmont:

    bridge_client: BridgeClient
    serial_client: SerialClient
    api_client: ApiClient
    port: str
    baudrate: int
    serial_timeout: int = 1
    logger = create_console_logger('Piedmont')
    debug: bool

    def __init__(
            self, name: str = None,
            address: str = None,
            port: str = None,
            baudrate: int = None,
            ** options
    ) -> None:
        super().__init__()
        self.bridge_client = BridgeClient(name, address)

        if port and baudrate:
            self.logger.info(
                f'Config serial with port:{port}, baudrate:{baudrate}')
            self.serial_client = SerialClient(port, baudrate)

        self.port = port
        self.baudrate = baudrate
        self._config(options=options)

    def send_pp_connection(self, value):
        self._send_pp_connection = value

    def _config(self, **options):
        self.debug = options.get('debug', False)
        if self.debug:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)

    def bridge(self, messageId: str, **options: t.Any):
        def decorator(func):

            self.bridge_client.regist_bridge_handler(messageId.upper(), func)

            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper

        return decorator

    def send_pp_connection(self, messageId: str, value: T_PP_Message_Payload):
        self.bridge_client.send(messageId.upper(), value)

    def send_serial(self):
        pass

    def send_api(self):
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
