class StoreError(Exception):
    def __init__(self, message):
        self.message = message


class StoreNotFound(StoreError):
    pass
