from __future__ import annotations

import typing as t
from pprint import pprint
import json

from . import logger


def _convert_key(key: str):
    if key.isdigit():
        return int(key)

    return key


class BaseStorage:
    _stack: list = []
    _array: list = []
    _data: dict = {}

    @property
    def stack_count(self):
        return len(self.stack)

    @property
    def list_count(self):
        return len(self.array)

    @property
    def data_count(self):
        return len(self.data.keys())

    @property
    def array(self):
        return self._array

    @property
    def stack(self):
        return self._stack

    @property
    def data(self):
        return self._data

    def append(self, obj: t.Any | t.Iterable):
        if isinstance(obj, list):
            self.array.extend(obj)
        else:
            self.array.append(obj)

    def insert(self, obj: any, index=0):
        if index == -1:
            self.array.append(obj)
        else:
            self.array.insert(index, obj)

    def keys(self):
        return self.data.keys()

    def push(self, obj: t.Any | t.Iterable[list]):
        if isinstance(obj, list):
            for item in obj:
                self.stack.append(item)
        else:
            self.stack.append(obj)

    def pop(self) -> any:
        return self.stack.pop()

    def peek(self) -> any:
        return self.stack[-1]

    def clear(self, target: t.Literal['stack', 'array', 'data'] = 'data'):
        if target == 'stack':
            self._stack = []
        elif target == 'array':
            self._array = []
        else:
            self._data = {}

    def show_data(self):
        print('=' * 10, 'DICT DATA', '=' * 10)
        pprint(self.data)

    def show_stack(self):
        print('=' * 10, 'STACK DATA', '=' * 10)
        pprint(self.stack)

    def show_array(self):
        print('=' * 10, 'ARRAY DATA', '=' * 10)
        pprint(self.array)


class Storage(BaseStorage):

    def _set_value_by_key_chain(self, key_chain: list[str], value: any):
        if key_chain[0].isdigit():
            current = self.array
        else:
            current = self.data

        for subkey in key_chain[:-1]:
            if subkey.isdigit():
                current = current[int(subkey)]
            else:
                try:
                    current = current[subkey]
                except KeyError:
                    current[subkey] = {}
                    current = current[subkey]

        try:
            current[_convert_key(key_chain[-1])] = value
        except IndexError:
            logger.error(
                f'Index out of length for key: `{'.'.join(key_chain)}`.')

    def set_value_by_key(self, key: str, value: any, type: t.Literal['text', 'json'] = 'text'):
        key_chain = key.split('.')
        if type == 'json':
            value = json.loads(value)

        if len(key_chain) > 1:
            self._set_value_by_key_chain(key_chain, value)
        else:
            self.data[key] = value

    def get_value_by_key(self, key: str) -> str:
        key_chain = key.split('.')
        try:
            if len(key_chain) > 1:
                return self._get_value_by_key_chain(key_chain)
            else:
                return self.data[key]
        except KeyError:
            logger.info(
                f'Can not find value for key: `{key}`, return empty string instead.')
            return ""

    def _get_value_by_key_chain(self, key_chain: list[str]) -> any:
        current = self.data
        for key in key_chain:
            if isinstance(current, list) and key.isdigit():
                key = int(key)
            current = current[key]
        return current

    def get_value_at_index(self, idx: str | int) -> str:
        if isinstance(idx, str) and not idx.isdigit():
            logger.warning(
                f'Index `{idx}` is not a number. return empty string instead.')
            return ""
        try:
            return self.array[int(idx)]
        except IndexError:
            logger.info(
                f'Index `{id}` is out of range. return empty string instead.')
            return ""


storage = Storage()
