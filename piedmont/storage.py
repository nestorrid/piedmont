from __future__ import annotations

import typing as t
from pprint import pprint
import json

from . import logger


def _convert_key(key: str):
    if _is_valid_number_string(key):
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

    def append(self, obj: t.Any, key: str = None):

        try:
            self.array.append(json.loads(obj))
        except json.decoder.JSONDecodeError:
            self.array.append(obj)

    def insert(self, obj: any, index=0):
        try:
            self.array.insert(index, json.loads(obj))
        except json.decoder.JSONDecodeError:
            self.array.insert(index, obj)

    def keys(self):
        return self.data.keys()

    def push(self, obj: t.Any):
        try:
            self.stack.append(json.loads(obj))
        except json.decoder.JSONDecodeError:
            self.stack.append(obj)

    def pop(self) -> any:
        return self.stack.pop()

    def peek(self) -> any:
        return self.stack[-1]

    def clear(self, target: t.Literal['stack', 'array', 'dict'] = 'dict'):
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

    def _set_value_by_key_chain(
        self, key_chain: list[str],
        value: any
    ):
        if _is_valid_number_string(key_chain[0]):
            current = self.array
        else:
            current = self.data

        for subkey in key_chain[:-1]:
            if _is_valid_number_string(subkey):
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
            raise IndexError(
                f'Index out of length for key: `{'.'.join(key_chain)}`.')

    def set_value_by_key(
            self, key: str, value: any,
    ):
        key_chain = key.split('.')

        try:
            data = json.loads(value)
        except json.decoder.JSONDecodeError:
            data = value

        if len(key_chain) > 1:
            self._set_value_by_key_chain(key_chain, data)
        else:
            self.data[key] = data

    def get_value_by_key(self, key: str) -> str:
        key_chain = key.split('.')
        try:
            if len(key_chain) > 1:
                return self._get_value_by_key_chain(key_chain)
            else:
                return self.data[key]
        except KeyError:
            raise KeyError(
                f'Can not find value for key: `{key}`.')

    def _get_value_by_key_chain(self, key_chain: list[str]) -> any:
        current = self.data
        for key in key_chain:
            if isinstance(current, list) and _is_valid_number_string(key):
                key = int(key)
            current = current[key]
        return current

    def get_value_at_index(self, idx: str | int) -> str:
        try:
            index = int(idx)
            return self.array[index]
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
