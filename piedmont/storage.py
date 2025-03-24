from __future__ import annotations

import typing as t
from pprint import pprint
import json

from . import logger
from .errors import KeyPathError


def _convert_key(key: str):
    if _is_valid_number_string(key):
        return int(key)

    return key


def _safe_load_json(data: any):
    try:
        data = json.loads(str(data))
    except json.decoder.JSONDecodeError:
        pass
    finally:
        return data


class BaseStorage:
    _stack: t.Dict[str, t.List[t.Any]] = {
        "default": []
    }
    _queue: t.Dict[str, t.List[t.Any]] = {
        "default": []
    }
    _list: t.Dict[str, t.List[t.Any]] = {
        'default': []
    }
    _dict: dict = {}

    def stack_count(self, key: str = 'default'):
        return len(self.stack(key))

    def queue_count(self, key: str = 'default'):
        return len(self.queue(key))

    def list_count(self, key: str = 'default'):
        return len(self.list(key))

    def dict_count(self):
        return len(self.dict.keys())

    def list(self, key: str = 'default') -> t.List[t.Any] | None:
        return self._list.get(key, None)

    def stack(self, key: str = 'default') -> t.List[t.Any] | None:
        return self._stack.get(key, None)

    def queue(self, key: str = 'default') -> t.List[t.Any] | None:
        return self._queue.get(key, None)

    @property
    def dict(self) -> t.Dict[str, t.Any]:
        return self._dict

    @property
    def keys(self) -> t.List[str]:
        return self.dict.keys()

    def append(self, obj: t.Any, key: str = 'default') -> t.List[t.Any]:
        data = _safe_load_json(obj)
        self._list[key] = self.list(key) or []
        self._list[key].append(data)
        return self.list(key)

    def insert(self, obj: any, index=0, key: str = 'default') -> t.List[t.Any]:
        data = _safe_load_json(obj)
        self._list[key] = self.list(key) or []
        self._list[key].insert(index, data)
        return self.list(key)

    def remove(self, obj: any, key: str = 'default'):
        l = self.list(key) or []
        try:
            l.remove(obj)
        except ValueError:
            pass

    def push(
            self, obj: t.Any,
            target: t.Literal['stack', 'queue'] = 'stack',
            key: str = 'default'
    ) -> int:
        data = _safe_load_json(obj)
        if target == 'stack':
            self._stack[key] = self.stack(key) or []
            self._stack[key].append(data)
            return len(self.stack(key))
        else:
            self._queue[key] = self.queue(key) or []
            self._queue[key].append(data)
            return len(self.queue(key))

    def pop(
        self,
        target: t.Literal['stack', 'queue'] = 'stack',
        key: str = 'default'
    ) -> any:
        if target == 'stack':
            return self.stack(key).pop()
        else:
            return self.queue(key).pop(0)

    def peek(
        self,
        target: t.Literal['stack', 'queue'] = 'stack',
        key: str = 'default'
    ) -> any:
        if target == 'stack':
            return self.stack(key)[-1]
        else:
            return self.queue(key)[0]

    def clear(self, target: t.Literal['stack', 'list', 'dict', 'queue'] = 'dict'):
        if target == 'stack':
            self._stack = {
                "default": []
            }
        elif target == 'list':
            self._list = {
                "default": []
            }
        elif target == 'queue':
            self._queue = {
                'default': []
            }
        else:
            self._dict = {}

    def show_dict(self):
        print('=' * 10, 'DICT DATA', '=' * 10)
        pprint(self.dict)

    def show_stack(self):
        print('=' * 10, 'STACK DATA', '=' * 10)
        pprint(self._stack)

    def show_list(self):
        print('=' * 10, 'LIST DATA', '=' * 10)
        pprint(self._list)

    def show_queue(self):
        print('=' * 10, 'QUEUE DATA', '=' * 10)
        pprint(self._queue)


class Storage(BaseStorage):

    def _set_value_by_key_path(
        self, key_path: list[str],
        value: any
    ):
        current = self.dict

        for subkey in key_path[:-1]:
            if _is_valid_number_string(subkey):
                current = current[int(subkey)]
            else:
                try:
                    current = current[subkey]
                except KeyError:
                    current[subkey] = {}
                    current = current[subkey]

        try:
            current[_convert_key(key_path[-1])] = value
        except IndexError:
            raise IndexError(
                f'Index out of length for key: `{'.'.join(key_path)}`.')

    def set_value_by_key(
            self, key: str, value: any,
    ):
        key_path = key.split('.')

        data = _safe_load_json(value)

        if len(key_path) > 1:
            if _is_valid_number_string(key_path[0]):
                raise KeyPathError(key)

            self._set_value_by_key_path(key_path, data)
        else:
            self.dict[key] = data

    def get_value_by_key(self, key: str) -> str:
        key_path = key.split('.')
        try:
            if len(key_path) > 1:
                if _is_valid_number_string(key_path[0]):
                    raise KeyPathError(key)

                return self._get_value_by_key_path(key_path)
            else:
                return self.dict[key]
        except KeyError:
            raise KeyError(
                f'Can not find value for key: `{key}`.')

    def _get_value_by_key_path(self, key_path: list[str]) -> any:
        current = self.dict
        for key in key_path:
            if isinstance(current, list) and _is_valid_number_string(key):
                key = int(key)
            current = current[key]
        return current

    def get_value_at_index(self, idx: str | int) -> str:
        try:
            index = int(idx)
            return self.list()[index]
        except ValueError:
            raise ValueError(f'Index `{idx}` is not a number.')
        except IndexError:
            raise IndexError(f'Index `{idx}` is out of range.')


def _is_valid_number_string(num: str) -> bool:
    try:
        temp = int(num)
        return True
    except ValueError:
        return False


storage = Storage()
