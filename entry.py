class Entry:
    def __init__(self, key: object, value: object, target_bucket: int):
        self._key = key
        self._value = value
        self._bucket = target_bucket
        self._next = -1


