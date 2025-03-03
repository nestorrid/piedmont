from __future__ import annotations
import typing as t

import serial
import threading

from .errors import ConfigError, DuplicateHandlerError
from .typing import T_Handler
from .logger import logger


class SerialClient:

    ser: serial.Serial = None
    handler_mapper = {}

    def __init__(self, config: t.Dict):
        self.port = config.get('port', None)
        self.baudrate = config.get('baudrate', 115200)
        self.timeout = config.get('timeout', 1)
        self.separator = config.get('separator', "::")
        self.connect()
        if self.ser and self.ser.is_open:
            self.start_reading_serial()

    def regist_serial_handler(self, messageId: str, handler: T_Handler):
        old_handler = self.handler_mapper.get(messageId, None)
        if old_handler:
            raise DuplicateHandlerError(messageId)
        self.handler_mapper[messageId] = handler

    def connect(self):
        if not self.port:
            logger.warning('No port specified. Skip Serial connection.')
            return

        try:
            self.ser = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=self.timeout
            )
            logger.info(
                f'Connected to port: {self.port}, baudrate: {self.baudrate}')
        except serial.SerialException as e:
            logger.error(f'Serial error: {e}')

    def disconnect(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
            logger.info(f'Disconnect from port {self.port}')

    def __del__(self):
        self.disconnect()

    def _reading_serial(self):
        logger.info(f'Start listening on port {format(self.port)}.')
        try:
            while True:
                if self.ser.in_waiting:
                    data = self.ser.readline().decode('utf-8').rstrip()
                    logger.debug(f'Receive data from serial: {data}')

                    result = data.split(self.separator)

                    if len(result) != 2:
                        logger.debug(f'Can not parse serial data: {data}')
                        continue

                    handler = self.handler_mapper.get(result[0])
                    if handler:
                        logger.debug(
                            f'Receive serial message: `{result[0]}` with data: `{result[1]}`')
                        logger.info(
                            f'Handle message: `{result[0]}` with handler: `{handler.__name__}`')
                        handler(result[1])

        except KeyboardInterrupt as e:
            logger.info('Serial listening interrupted by user.')
        finally:
            self.disconnect()

    def start_reading_serial(self):
        thread = threading.Thread(target=self._reading_serial)
        thread.daemon = True
        thread.start()
