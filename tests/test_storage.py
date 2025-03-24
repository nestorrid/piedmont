import pytest
from piedmont.storage import Storage, _is_valid_number_string


@pytest.fixture(scope='function')
def storage():
    s = Storage()
    s._list['default'] = [f'test{i}' for i in range(5)]
    s._stack['default'] = [f'string{i}' for i in range(5)]
    s._queue['default'] = [f'task{i}' for i in range(5)]
    s._dict = {f'key{i}': f'value{i}' for i in range(5)}
    return s


def test_append_storage_will_add_to_array(storage):
    count = storage.list_count()
    storage.append('test')
    assert storage.list_count() == count + 1


def test_push_object_will_add_to_stack(storage):
    count = storage.stack_count()
    storage.push('test')
    assert storage.stack_count() == count + 1


def test_pop_object_will_remove_last_object_in_stack(storage):
    last = storage.stack()[-1]
    count = storage.stack_count()
    obj = storage.pop()
    assert obj == last
    assert storage.stack_count() == count - 1


def test_peek_will_return_last_object_but_not_remove(storage):
    count = storage.stack_count()
    result = storage.peek()
    assert result == storage.stack()[-1]
    assert storage.stack_count() == count


def test_set_value_by_string_key_chain(storage):
    storage._dict = {
        # 'key1': {
        #     'key2': {}
        # }
    }
    storage.set_value_by_key('key1.key2.key3', 'new value')
    assert storage._dict['key1']['key2']['key3'] == 'new value'


def test_set_value_by_key_chain_with_idx_as_first_key(storage):
    from piedmont.errors import KeyPathError
    with pytest.raises(KeyPathError) as exc_info:
        storage.set_value_by_key('0.key1.key2', 'value')

    assert exc_info.type == KeyPathError


def test_set_value_by_key_chain_with_idx_as_last_key(storage):
    storage._dict = {
        'key1': {
            'key2': [
                1, 2, 3, 4, 5
            ]
        }
    }
    storage.set_value_by_key('key1.key2.3', 100)
    print(storage.dict)
    assert storage.dict['key1']['key2'][3] == 100


def test_set_json_value_by_key_will_convert_to_object(storage):
    storage.set_value_by_key('test.key', '[1,2,3,4,5]')
    assert isinstance(storage.dict['test']['key'], list)
    assert len(storage.dict['test']['key']) == 5


def test_set_value_by_single_key(storage):
    storage.set_value_by_key('test key', 'test_value')
    assert storage.dict['test key'] == 'test_value'


def test_clear_data(storage):
    storage.clear()
    assert storage.dict_count() == 0
    storage.clear('list')
    assert storage.list_count() == 0
    storage.clear('queue')
    assert storage.queue_count() == 0
    storage.clear('stack')
    assert storage.stack_count() == 0


def test_get_value_by_none_digit_index(storage):
    with pytest.raises(ValueError) as exc_info:
        result = storage.get_value_at_index('index')
    assert exc_info.type == ValueError


def test_get_value_by_index(storage):
    result = storage.get_value_at_index(3)
    assert result == storage.list()[3]
    result = storage.get_value_at_index('2')
    assert result == storage.list()[2]


def test_show_data(storage):
    storage.show_dict()
    storage.show_list()
    storage.show_stack()
    storage.show_queue()


def test_get_value_by_single_key(storage):
    result = storage.get_value_by_key('key1')
    assert result == 'value1'


def test_get_value_by_key_chain(storage):
    storage._dict = {
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


def test_append_object_with_key(storage):
    storage.append('test', 'key')
    storage.show_list()
    assert storage.list_count('key') == 1


def test_push_object_with_key(storage):
    storage.push('value1', key='key')
    storage.push('value2', key='key')
    storage.show_stack()
    assert storage.stack_count('key') == 2
    assert storage._stack['key'][1] == 'value2'


def test_remove_from_list(storage):
    storage.clear('list')
    for i in range(5):
        storage.append(f'test{i}')

    storage.remove('test3')
    storage.show_list()
    assert storage.list_count() == 4
    storage.append('new value', 'key')
    assert storage.list_count('key') == 1
    storage.remove('new value', 'key')
    assert storage.list_count('key') == 0
    storage.remove('none exists')
    assert storage.list_count() == 4


def test_append_into_and_pop_from_queue(storage):
    storage.clear('queue')
    for i in range(5):
        storage.push(f'data{i}', 'queue')

    assert storage.queue_count() == 5

    result = storage.pop('queue')
    assert result == 'data0'
