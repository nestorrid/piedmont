from piedmont.app import _key_index_parser


def test_insert_key_handelr():
    data = {
        'key': 'key1.key2'
    }
    key, idx = _key_index_parser(data)
    assert key == 'key1.key2'
    assert idx == 0

    data = {
        'key': 'key1.key2.1'
    }
    key, idx = _key_index_parser(data)
    assert key == 'key1.key2'
    assert idx == 1

    data = {
        'key': '3'
    }
    key, idx = _key_index_parser(data)
    assert key == 'default'
    assert idx == 3