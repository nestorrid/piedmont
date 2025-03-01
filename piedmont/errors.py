class DuplicateHandlerError(Exception):
    def __init__(self, name):
        super().__init__(f"Duplicate handler for message:{name}")
