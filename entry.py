class Entry(object):
    def __init__(self, key: object, value: object, target_bucket: int, next: int = -1):
        self._key = key
        self._value = value
        self._bucket = target_bucket
        self._next = next

    @staticmethod
    def get_entry_by_string(json_string):
        return Entry(json_string['_key'], json_string['_value'], json_string['_bucket'], json_string['_next']) if json_string else None

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


