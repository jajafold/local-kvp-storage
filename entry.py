class Entry:
    def __init__(self, key: object, value: object, target_bucket: int, next: int = -1):
        self._key = key
        self._value = value
        self._bucket = target_bucket
        self._next = next

    @property
    def bucket(self):
        return self._bucket

    @property
    def next(self):
        return self._next

    @property
    def key(self):
        return self._key

    @property
    def value(self):
        return self._value


