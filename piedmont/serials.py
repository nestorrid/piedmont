from __future__ import annotations
import typing as t

import serial
import threading
from .logger import create_console_logger


class SerialClient:

    ser: serial.Serial
    is_connected = False
    logger = create_console_logger('SerialClient')

    def __init__(self, port: str = None, baudrate: int = None, timeout: int = 1):
        self.port = port
        self.baudrate = baudrate

    def connect(self):
        try:
            self.ser = serial.Serial(self.port, self.baudrate, self.timeout)
            self.is_connected = True
            self.logger.info(
                f'Connected to port: {self.port}, baudrate: {self.baudrate}')
        except serial.SerialException as e:
            self.logger.error(f'Serial error: {e}')

    def disconnect(self):
        self.ser.close()
        self.is_connected = False

    def __del__(self):
        pass
        # self.disconnect()

    def _reading_serial(self):
        try:
            while True:
                if self.ser.in_waiting:
                    data = self.ser.readline().decode('utf-8').rstrip()
                    self.logger.info(f'Receive data from serial: {data}')
        except KeyboardInterrupt as e:
            self.logger.info('Serial listening interrupted by user.')
        finally:
            self.ser.close()

    def _fake_read_serial(self):
        try:
            while True:
                data = input('> Fake serial reading message:')
                self.logger.info(f'Receive data from serial: {data}')
        except KeyboardInterrupt as e:
            self.logger.info('Serial listening interrupted by user.')
        finally:
            self.ser.close()

    def start_reading_serial(self, debug=False):
        if debug:
            thread = threading.Thread(target=self._fake_read_serial)
        else:
            thread = threading.Thread(target=self._reading_serial)
        thread.daemon = True
        thread.start()
