from __future__ import annotations

import typing as t
import json
import functools
import socketio
import socketio.exceptions

from .config import Config
from .typing import T_Handler, T_Mapper
from .errors import DuplicateHandlerError
from .storage import storage
from . import logger

PP_BRIDGE_APP = 'ppBridgeApp'
PP_MESSAGE = 'ppMessage'


class Piedmont():

    _client = socketio.Client()
    _config: Config
    _handler_mapper: T_Mapper

    def __init__(
            self,
            config: Config = None,
            debug: bool = False,
            auto_connect: bool = True,
            separator: str = "::"
    ) -> None:
        super().__init__()
        self._handler_mapper = {}
        logger.set_dev_mode(debug)
        self._config = config or Config()
        self.separator = separator
        self._regist_handlers()
        self._regist_data_handlers()
        if auto_connect:
            self.connect()

    def _regist_data_handlers(self):
        self._handler_mapper.setdefault(
            'pie.push', self._push
        )
        self._handler_mapper.setdefault(
            'pie.pop', self._pop
        )
        self._handler_mapper.setdefault(
            'pie.append', self._append
        )

    def _append(self, data):
        storage.append(data)

    def _push(self, data):
        storage.push(data)

    def _pop(self, data):
        result = storage.pop()
        self.send('popout', result)

    def _regist_handlers(self):
        self._client.on(PP_MESSAGE, self._message_handler)
        self._client.on('connect', self._client_connect)
        self._client.on('disconnect', self._client_disconnect)

    def _dynamic_message_handler(self, message: str, data):
        temp = message.split(self.separator)
        cmd = temp[0]
        key = temp[1]
        if cmd == 'pie.set':
            storage.set_value_by_key(key, data.get('value', None))
        elif cmd == 'pie.setJson':
            storage.set_value_by_key(key, data.get('value', None), 'json')
        elif cmd == 'pie.get':
            pass
        elif cmd == '':
            storage.append(data)

        self.send('data', json.dumps(storage._data))
        self.send('stack', json.dumps(storage._stack))
        self.send('array', json.dumps(storage._array))

    def _message_handler(self, data):
        msgId = data['messageId']
        if len(msgId.split(self.separator)) > 1:
            self._dynamic_message_handler(msgId, data)
            return

        handler = self._handler_mapper.get(msgId, None)
        if handler:
            logger.info(f'Receive message from ProtoPie Connect.')
            logger.info(f'Message: `{msgId}`. Data: `{data}`.')
            logger.devlog(f'Handler: `{handler.__name__}`.')
            handler(data.get('value', None))
        else:
            logger.devlog(f'No handler for message: "{msgId}"')

    def _client_disconnect(self, data: t.Any = None):
        logger.info(
            f'Disconnect from: "{self._config.server}". {data or ""}')

    def _client_connect(self, data: t.Any = None):
        logger.info(f'Connect to: "{self._config.server}". {data or ""}')
        self._client.emit(PP_BRIDGE_APP, {'name': self._config.app_name})

    def connect(self):
        try:
            self._client.connect(self._config.server)
        except socketio.exceptions.ConnectionError as e:
            logger.error(
                f'Opps. Error occurred when connecting to server.\n'
                f'Error message: `{e}`.\n'
                f'Please open `ProtoPie Connect` before start.'
            )
            raise SystemExit(1)

    def bridge(self, messageId: str, **options: t.Any):
        def decorator(func):
            self._regist_bridge_handler(messageId, func)

            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper
        return decorator

    def storage(self, messageId: str):
        def decorator(func):
            self._regist_bridge_handler(messageId+self.separator, func)

            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper
        return decorator

    def _regist_bridge_handler(self, messageId: str, handler: T_Handler):
        old_func = self._handler_mapper.get(messageId, None)
        if old_func:
            raise DuplicateHandlerError(messageId)

        self._handler_mapper[messageId] = handler

    def send(self, messageId: str, value: t.Union[str, t.List[t.Any], t.Dict[t.AnyStr, t.Any]] = ""):

        if isinstance(value, str):
            data = value
        else:
            data = json.dumps(value)

        logger.info(f'Sending message to ProtoPie Connect.')
        logger.info(f'Message: `{messageId}`.')
        logger.info(f'Value: `{data}`')

        self._client.emit(
            PP_MESSAGE, {'messageId': messageId, 'value': data})

    def __del__(self):
        self._client.disconnect()
