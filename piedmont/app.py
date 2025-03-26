from __future__ import annotations

import typing as t
import json
import functools
import socketio
import socketio.exceptions

from .config import Config
from .typing import T_Handler, T_Mapper
from .errors import DuplicateHandlerError, KeyPathError, StackNotExists
from .storage import storage
from . import logger

PP_BRIDGE_APP = 'ppBridgeApp'
PP_MESSAGE = 'ppMessage'

BUILD_IN_MESSAGES = [
    # build in stack commands.
    ['pie.push', '_push'],
    ['pie.pop', '_pop'],
    ['pie.peek', '_peek'],
    # Build in queue commands.
    ['pie.pushq', '_q_push'],
    ['pie.popq', '_q_pop'],
    ['pie.peekq', '_q_peek'],
    # build in list commands.
    ['pie.insert', '_insert'],
    ['pie.append', '_append'],
    ['pie.index', '_index'],
    ['pie.remove', '_remove'],
    # ['pie.update', '_update'],
    # ['pie.sort', '_sort'],
    # ['pie.filter', '_filter'],
    # ['pie.count', '_count'],
    # ['pie.sum', '_sum'],
    # ['pie.avg', '_avg'],
    # build in dict commands.
    ['pie.set', '_set_value_by_key'],
    ['pie.get', '_get_value_by_key'],
    # build in data display commands.
    ['pie.list', '_show_list'],
    ['pie.stack', '_show_stack'],
    ['pie.queue', '_show_queue'],
    ['pie.dict', '_show_dict'],
    # help message.
    ['pie.help', '_show_help'],
    ['pie.clear', '_clear']
]


def _safe_load_key(data: any):
    if isinstance(data, dict) and 'key' in data and 'piedmont.payload' in data:
        return data['key']
    return 'default'


def _safe_load_data(data: any):
    if isinstance(data, dict) and 'value' in data and 'piedmont.payload' in data:
        return data['value']
    return data


def _is_invalid_key(data: any):
    return not isinstance(data, dict) \
        or not 'key' in data \
        or len(data['key']) == 0


def _key_index_parser(data: any):
    key = str(data.get('key', None))
    if key:
        key_path = key.split('.')
        idx = key_path.pop()
        if not idx.isdigit():
            idx = 0
        else:
            idx = int(idx)
            if len(key_path) == 0:
                key = 'default'
            else:
                key = '.'.join(key_path)
    else:
        key = 'default'
        idx = 0
    return key, idx


class Piedmont():

    _client = socketio.Client()
    _config: Config
    _handler_mapper: T_Mapper

    def __init__(
            self,
            config: Config = None,
            debug: bool = False,
            auto_connect: bool = False,
            separator: str = "::"
    ) -> None:
        super().__init__()
        self._handler_mapper = {}
        logger.set_dev_mode(debug)
        self._config = config or Config()
        self.separator = separator
        self._regist_handlers()
        self._regist_buildin_handlers()
        if auto_connect:
            self.connect()

    def start(self):
        try:
            if not self._client.connected:
                self.connect()

            while self._client.connected:
                pass
        except KeyboardInterrupt:
            if self._client.connected:
                self._client.disconnect()

    def _regist_buildin_handlers(self):
        for buildin in BUILD_IN_MESSAGES:
            self._handler_mapper.setdefault(
                buildin[0],
                getattr(self, buildin[1])
            )

    def _set_value_by_key(self, data):
        if _is_invalid_key(data):
            self._error_message(
                f'You need to provide a key for `pie.set`, like `pie.set{self.separator}key`'
            )
            return

        key = data['key']
        value = data['value']
        try:
            result = storage.set_value_by_key(key, value)
            self.send(f'key::{key}', result)
        except KeyPathError as e:
            self._error_message(f'{e}')

    def _get_value_by_key(self, data):
        try:
            result = storage.get_value_by_key(data['key'])
            logger.debug(data)
            self.send(f'key::{data['key']}', result)
        except KeyError as e:
            self._error_message(f'{e}')

    def _show_help(self, data):
        pass

    def _show_stack(self, data):
        self.send('stack.all', storage._stack)

    def _show_dict(self, data):
        self.send('dict.all', storage.dict)

    def _show_list(self, data):
        self.send('list.all', storage._list)

    def _show_queue(self, data):
        self.send('queue.all', storage._queue)

    def error(self, msg: str):
        self.send('pie.error', msg)

    def _push(
            self, data,
            target: t.Literal['stack', 'queue'] = 'stack',
    ):
        logger.debug(f'push data: `{data}`, type of data: {type(data)}')
        result = storage.push(
            _safe_load_data(data),
            target,
            _safe_load_key(data)
        )
        self.send(f'push.{_safe_load_key(data)}', result)

    def _pop(
        self, data,
        target: t.Literal['stack', 'queue'] = 'stack',
    ):
        try:
            key = _safe_load_key(data)
            try:
                idx = int(_safe_load_data(data))
            except ValueError:
                idx = None
            except TypeError:
                idx = None
            result = storage.pop(target, key, idx)
            self.send(f'pop.{key}', result)
        except IndexError:
            logger.info(f'{target}.{key} storage is empty.')
            self.send(f'pop.{key}.empty')
        except StackNotExists as e:
            self._error_message(f'{e}')

    def _peek(
        self, data,
        target: t.Literal['stack', 'queue'] = 'stack',
        key: str = 'default'
    ):
        try:
            result = storage.peek(target, _safe_load_key(data))
            self.send(f'peek.{_safe_load_key(data)}', result)
        except IndexError:
            logger.info(f'{target}.{_safe_load_key(data)} storage is empty.')
            self.send(f'peek.{_safe_load_key(data)}.empty')

    def _q_push(self, data):
        self._push(data, 'queue')

    def _q_pop(self, data):
        self._pop(data, 'queue')

    def _q_peek(self, data):
        self._peek(data, 'queue')

    def _append(self, data):
        logger.debug(f'- ACTION: append data: `{data}`')
        result = storage.append(
            _safe_load_data(data),
            _safe_load_key(data)
        )
        self.send(f'append.{_safe_load_key(data)}', result)
        logger.debug(f'{storage._list}')

    def _insert(self, data):
        logger.debug(f'- ACTION: insert data: `{data}`')
        if isinstance(data, dict):
            value = data.get('value', None)
            key, idx = _key_index_parser(data)
        else:
            value = data
            idx = 0
            key = 'default'

        logger.debug(f'value type: {type(value)}')

        if not value:
            self._error_message(
                f'You must provide a valid value for `pie.insert`')
            return

        result = storage.insert(value, idx, key)
        self.send(f'insert.{key}', result)
        logger.debug(f'{storage._list}')

    def _index(self, data):
        logger.debug(f' - ACTION: obj at index: `{data}`')
        try:
            if isinstance(data, dict):
                idx = int(data['value'])
                key = data['key']
            else:
                idx = int(data)
                key = 'default'
            result = storage.index(idx, key)
            self.send(f'index.{key}', {'index': idx, 'value': result})
        except IndexError as e:
            self._error_message(f'{e}')
        except ValueError as e:
            k = data
            if isinstance(data, dict):
                k = data['value']
            self._error_message(f'`{k}` is not a valid index.')

    def _remove(self, data):
        logger.debug(f' - ACTION: remove obj at index: `{data}`')
        try:
            if isinstance(data, dict):
                idx = int(data['value'])
                key = data['key']
            else:
                idx = int(data)
                key = 'default'
            result = storage.remove(idx, key)
            self.send(f'remove.{key}', {'index': idx, 'value': result})
            logger.debug(f'{storage.list(key)}')
        except KeyError as e:
            self._error_message(f'{e}')
        except IndexError as e:
            self._error_message(f'{e}')
        except ValueError as e:
            print(e.args)
            k = data
            if isinstance(data, dict):
                k = data['value']
            self._error_message(f'`{k}` is not a valid index.')

    def _error_message(self, msg):
        logger.warning(msg)
        self.error(msg)

    def _regist_handlers(self):
        self._client.on(PP_MESSAGE, self._message_handler)
        self._client.on('connect', self._client_connect)
        self._client.on('disconnect', self._client_disconnect)

    def _dynamic_message_handler(self, message: str, data):
        temp = message.split(self.separator)
        cmd = temp[0]
        key = temp[1]

        handler = self._handler_mapper.get(cmd, None)
        if handler:
            logger.info(f'Receive dynamic message from ProtoPie Connect.')
            logger.info(
                f'Message: `{cmd}`, command key: `{key}`. Data: `{data}`.')
            logger.debug(
                f'Handler: `{handler.__module__}.{handler.__name__}`.')

            return handler({
                'key': key,
                'value': data.get('value', None),
                'piedmont.payload': True
            })
        else:
            logger.debug(f'No handler for message: "{cmd}"')

    def _message_handler(self, data):
        msgId = data['messageId']
        logger.debug(f'Receive message: `{msgId}`')
        if len(msgId.split(self.separator)) > 1:
            logger.debug(f'Message `{msgId}` is a dynamic message.')
            return self._dynamic_message_handler(msgId, data)

        handler = self._handler_mapper.get(msgId, None)
        if handler:
            logger.info(f'Receive message from ProtoPie Connect.')
            logger.info(f'Message: `{msgId}`. Data: `{data}`.')
            logger.debug(f'Handler: `{handler.__name__}`.')
            return handler(data.get('value', None))
        else:
            logger.debug(f'No handler for message: "{msgId}"')

    def _client_disconnect(self, data: t.Any = None):
        print(
            f'Disconnect from: "{self._config.server}". {data or ""}')

    def _client_connect(self, data: t.Any = None):
        print(f'Connect to: "{self._config.server}". {data or ""}')
        self._client.emit(PP_BRIDGE_APP, {'name': self._config.app_name})

    def connect(self):
        try:
            self._client.connect(self._config.server)
        except socketio.exceptions.ConnectionError as e:
            logger.error(f'Opps. Error occurred when connecting to server.')
            logger.error(f'Error message: `{e}`.')
            logger.error(f'Please open `ProtoPie Connect` before start.')
            raise SystemExit(1)

    def bridge(
        self,
        messageId: str,
        is_dynamic: bool = False,
    ):
        def decorator(func):
            key = messageId
            if is_dynamic:
                key = messageId + self.separator

            self._regist_bridge_handler(key, func)

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

    def _clear(self, data):
        storage.clear('all')

    def __del__(self):
        if self._client.connected:
            self._client.disconnect()
