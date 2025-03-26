class DuplicateHandlerError(Exception):
    def __init__(self, name):
        super().__init__(f"Duplicate handler for message:{name}")


class KeyPathError(Exception):
    def __init__(self, key: str):
        super().__init__(
            f'First key in key path can not be number. Check out the query key: `{key}`')


class StackNotExists(Exception):
    def __init__(self, key: str):
        super().__init__(
            f'The stack with name `{key}` doesn\'t exits.'
        )


class ConfigError(Exception):
    def __init__(self, message):
        super().__init__(message)
