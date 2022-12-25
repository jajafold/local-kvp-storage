from entry import Entry
from hashlib import sha256
import json


class Storage:
    def __init__(self):
        self._capacity = 29
        self.length = 0
        self._buckets = [-1 for _ in range(self._capacity)]
        self._entries = []
        self._encoder = json.encoder.JSONEncoder()

    def _encode_object(self, o: object) -> bytes:
        _encoded = self._encoder.encode(o)
        return _encoded.encode()

    def _compute_hash_and_bucket(self, key: object) -> (int, int):
        _sha256 = sha256(self._encode_object(key))
        _hash = int(_sha256.hexdigest(), 16) & 0x7FFFFFFF

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

    def _search_through_chain(self, key: object, entry: Entry) -> object:
        if entry.key != key:
            return self._search_through_chain(key, self._entries[entry.next])

        return entry

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
        _entry = None

        if self._buckets[_bucket] == -1:
            raise KeyError("Key not found")

        _entry = self._entries[self._buckets[_bucket]]
        if _entry.next != -1:
            _entry = self._search_through_chain(key, _entry)

        return _entry.value

    @property
    def keys(self):
        return [_entry.key for _entry in self._entries]

    @property
    def values(self):
        return [_entry.value for _entry in self._entries]




