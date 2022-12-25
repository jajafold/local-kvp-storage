from entry import Entry


class Storage:
    def __init__(self):
        self._capacity = 29
        self.length = 0
        self._buckets = [-1 for _ in range(self._capacity)]
        self._entries = []

    def _compute_hash_and_bucket(self, key: object) -> (int, int):
        _hash = key.__hash__() & 0x7FFFFFFF
        print(f"KEY: {key} | HASH: {_hash} | BUCKET: {_hash % self._capacity}")
        return _hash, _hash % self._capacity

    def _rehash(self):
        # TODO: реализовать функцию перехегирования таблицы
        raise NotImplementedError

    def _build_chain(self, key: object, value: object, bucket: int):
        _old_index = self._buckets[bucket]
        self._buckets[bucket] = self.length
        self.length += 1

        self._entries.append(Entry(key=key, value=value, target_bucket=bucket, next=_old_index))

    def add(self, key: object, value: object):
        if self.length == self._capacity:
            self._rehash()

        _hash, _bucket = self._compute_hash_and_bucket(key)
        if self._buckets[_bucket] != -1:
            self._build_chain(key, value, _bucket)
            return

        self._buckets[_bucket] = self.length
        self.length += 1

        self._entries.append(Entry(key=key, value=value, target_bucket=_bucket))

    def get_by(self, key: object) -> object:
        _hash, _bucket = self._compute_hash_and_bucket(key)
        _value = None

        if self._buckets[_bucket] == -1:
            raise KeyError("Key not found")

        _value = self._entries[self._buckets[_bucket]]
        return _value.value

    @property
    def keys(self):
        return [_entry.key for _entry in self._entries]

    @property
    def values(self):
        return [_entry.value for _entry in self._entries]




