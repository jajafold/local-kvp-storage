from entry import Entry


class Storage:
    def __init__(self):
        self._capacity = 10
        self.length = 0
        self._buckets = [-1 for _ in range(self._capacity)]
        self._entries = []

    def _compute_hash_and_bucket(self, key: object) -> (int, int):
        _hash = hash(key) & 0x7FFFFFFF
        return _hash, _hash % self._capacity

    def add(self, key: object, value: object):
        _hash, _bucket = self._compute_hash_and_bucket(key)
        self._buckets[_bucket] = self.length
        self._entries.append(Entry(key=key, value=value, target_bucket=_bucket))

    @property
    def keys(self):
        return [_entry.key for _entry in self._entries]

    @property
    def values(self):
        return [_entry.value for _entry in self._entries]




