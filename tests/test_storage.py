import pytest
from piedmont.storage import Storage, _is_valid_number_string


@pytest.fixture(scope='function')
def storage():
    s = Storage()
    s._array = [f'test{i}' for i in range(5)]
    s._stack = [f'string{i}' for i in range(5)]
    s._data = {f'key{i}': f'value{i}' for i in range(5)}
    return s


def test_append_storage_will_add_to_array(storage):
    count = storage.list_count
    storage.append('test')
    assert storage.list_count == count + 1


def test_push_object_will_add_to_stack(storage):
    count = storage.stack_count
    storage.push('test')
    assert storage.stack_count == count + 1


def test_pop_object_will_remove_last_object_in_stack(storage):
    last = storage._stack[-1]
    count = storage.stack_count
    obj = storage.pop()
    assert obj == last
    assert storage.stack_count == count - 1


def test_peek_will_return_last_object_but_not_remove(storage):
    count = storage.stack_count
    result = storage.peek()
    assert result == storage.stack[-1]
    assert storage.stack_count == count


def test_set_value_by_string_key_chain(storage):
    storage._data = {
        # 'key1': {
        #     'key2': {}
        # }
    }
    storage.set_value_by_key('key1.key2.key3', 'new value')
    assert storage._data['key1']['key2']['key3'] == 'new value'
    print(storage._data)


def test_set_value_by_key_chain_with_idx_as_first_key(storage):
    storage._array = [{'key': {'subkey': 'value'}} for _ in range(5)]
    print(storage._array)
    storage.set_value_by_key('3.key.subkey', 'new value')
    assert storage._array[3]['key']['subkey'] == 'new value'
    storage.set_value_by_key('3.key.newkey', 'new value')
    print(storage._array)


def test_set_value_by_key_chain_with_idx_as_last_key(storage):
    storage._data = {
        'key1': {
            'key2': [
                1, 2, 3, 4, 5
            ]
        }
    }
    storage.set_value_by_key('key1.key2.3', 100)
    print(storage._data)
    assert storage._data['key1']['key2'][3] == 100


def test_set_json_value_by_key_will_convert_to_object(storage):
    storage.set_value_by_key('test.key', '[1,2,3,4,5]', 'json')
    assert isinstance(storage._data['test']['key'], list)
    assert len(storage._data['test']['key']) == 5


def test_set_value_by_single_key(storage):
    storage.set_value_by_key('test key', 'test_value')
    assert storage._data['test key'] == 'test_value'


def test_clear_data(storage):
    storage.clear()
    assert storage.data_count == 0
    storage.clear('array')
    assert storage.list_count == 0
    storage.clear('stack')
    assert storage.stack_count == 0


def test_get_value_by_none_digit_index(storage):
    with pytest.raises(ValueError) as exc_info:
        result = storage.get_value_at_index('index')
    assert exc_info.type == ValueError


def test_get_value_by_index(storage):
    result = storage.get_value_at_index(3)
    assert result == storage.array[3]
    result = storage.get_value_at_index('2')
    assert result == storage.array[2]


def test_show_data(storage):
    storage.show_data()
    storage.show_array()
    storage.show_stack()


def test_get_value_by_single_key(storage):
    result = storage.get_value_by_key('key1')
    assert result == 'value1'


def test_get_value_by_key_chain(storage):
    storage._data = {
        'key1': {
            'key2': [
                1, 2, 3, 4, 5
            ]
        }
    }

    result = storage.get_value_by_key('key1.key2')
    assert isinstance(result, list)
    assert len(result) == 5
    result = storage.get_value_by_key('key1.key2.3')
    assert result == 4


def test_is_valid_number_string():
    assert _is_valid_number_string('asdf') == False
    assert _is_valid_number_string('123') == True
    assert _is_valid_number_string('-10') == True
