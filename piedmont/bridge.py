from __future__ import annotations

import socketio
import json
import logging

from .typing import T_Handler, T_Mapper, T_PP_Message_Payload
from .logger import create_console_logger
from .errors import DuplicateHandlerError

PP_BRIDGE_APP = 'ppBridgeApp'
PP_MESSAGE = 'ppMessage'


class BridgeClient:

    client = socketio.Client()
    name: str
    address: str
    handler_mapper: T_Mapper
    logger = create_console_logger('BridgeClient')

    def __init__(self, name, address):
        super().__init__()
        self.handler_mapper = {}
        self.app_name = name or 'Bridge App'
        self.address = address or 'http://localhost:9981'
        self._regist_handlers()
        self.client.connect(self.address)

    def _regist_handlers(self):
        self.client.on(PP_MESSAGE, self._message_handler)
        self.client.on('connect', self._client_connect)
        self.client.on('disconnect', self._client_disconnect)

    def _client_disconnect(self):
        self.logger.info(f'Disconnecting from: "{self.address}"')

    def _client_connect(self):
        self.logger.info(f'Connect to: "{self.address}"')
        self.client.emit(PP_BRIDGE_APP, {'name': self.app_name})

    def _message_handler(self, data):
        msgId = data['messageId'].upper()
        self.logger.debug(f'Receive message: "{msgId}"')
        handler = self.handler_mapper.get(msgId, None)
        if handler:
            self.logger.info(
                f'Receive message from ProtoPie Connect.\n\tMessage: `{msgId}`,\n\tData: `{data}`,\n\tHandler: `{handler.__name__}`')
            handler(data.get('value', None))
        else:
            self.logger.info(f'No handler for message: "{msgId}"')

    def regist_bridge_handler(self, messageId: str, handler: T_Handler):
        old_func = self.handler_mapper.get(messageId, None)
        if old_func:
            raise DuplicateHandlerError(messageId)

        self.handler_mapper[messageId] = handler

    def send(self, messageId: str, value: T_PP_Message_Payload):
        if isinstance(value, str):
            data = value
        else:
            data = json.dumps(value)

        self.logger.info(
            f'Sending message to ProtoPie Connect.\n\tMessage: `{messageId}`\n\tValue: `{data}`')

        self.client.emit(
            PP_MESSAGE, {'messageId': messageId, 'value': data})

    def __del__(self):
        self.client.disconnect()
