import os
import pathlib
from datetime import datetime
from entry import Entry
from hashlib import sha256
from jsonpickle import encode, loads


class Storage(object):
    def __init__(self, repository_name: str, capacity=29, dump_file_name: str = datetime.now().date()):
        self._dump_file_name = f"{dump_file_name}.json"
        self._repository = repository_name
        self._capacity = capacity
        self._max_capacity = 1000
        self.length = 0

        self.__initialize()

    def __initialize(self):
        self._buckets = [-1 for _ in range(self._capacity)]
        self._entries = []
        self._free = []

    def __rehash(self):
        self._capacity *= 2
        _dump_entries = [_entry for _entry in self._entries]

        self.__initialize()
        for _entry in _dump_entries:
            self.add(_entry.key, _entry.value)

    def __check_necessity(self) -> bool:
        if all([x == -1 for x in self._buckets]):
            return False
        else:
            return True

    @staticmethod
    def _encode_object(o: object) -> bytes:
        _encoded = encode(o)
        return _encoded.encode()

    def _compute_hash_and_bucket(self, key: object) -> (int, int):
        _sha256 = sha256(Storage._encode_object(key))
        _hash = int(_sha256.hexdigest(), 16) & 0x7FFFFFFF

        return _hash, _hash % self._capacity

    def _build_chain(self, key: object, value: object, bucket: int):
        _old_index = self._buckets[bucket]
        self._buckets[bucket] = len(self._entries)
        self.length += 1

        self._entries.append(Entry(key=key, value=value, target_bucket=bucket, next=_old_index))

    def _search_through_chain(self, key: object, entry: Entry) -> object:
        if entry.key != key:
            return self._search_through_chain(key, self._entries[entry.next])
        return entry

    def add(self, key: object, value: object):
        if self.length == self._capacity:
            self.__rehash()

        _hash, _bucket = self._compute_hash_and_bucket(key)
        if self._buckets[_bucket] != -1:

            if self._entries[self._buckets[_bucket]].key == key:
                raise KeyError("This key is already in storage")

            self._build_chain(key, value, _bucket)
            return

        if not self._free:
            self._buckets[_bucket] = len(self._entries)
            self.length += 1
            self._entries.append(Entry(key=key, value=value, target_bucket=_bucket))
        else:
            _free_index = self._free.pop(0)
            self._buckets[_bucket] = _free_index
            self.length += 1

            print(_free_index)
            self._entries[_free_index] = Entry(key=key, value=value, target_bucket=_bucket)

    def remove(self, key: object) -> bool:
        _hash, _bucket = self._compute_hash_and_bucket(key)
        _previous_entry = None

        if self._buckets[_bucket] == -1:
            raise KeyError("Key not found")

        _entry_to_delete = self._entries[self._buckets[_bucket]]
        while _entry_to_delete.key != key:
            _previous_entry = _entry_to_delete
            _entry_to_delete = self._entries[_entry_to_delete.next]

        self.length -= 1

        if _previous_entry:
            self._entries[_previous_entry._next] = None
            self._free.append(_previous_entry._next)

            _next_entry = _entry_to_delete.next
            _previous_entry._next = _next_entry
        else:
            _next_entry = _entry_to_delete.next
            self._entries[self._buckets[_bucket]] = None
            self._free.append(self._buckets[_bucket])

            self._buckets[_bucket] = _next_entry

        return self.__check_necessity()

    def _get_entry_by(self, key: object) -> Entry:
        _hash, _bucket = self._compute_hash_and_bucket(key)
        _entry = None

        if self._buckets[_bucket] == -1:
            raise KeyError("Key not found")

        _entry = self._entries[self._buckets[_bucket]]
        if _entry.next != -1:
            _entry = self._search_through_chain(key, _entry)

        return _entry

    def _get_by(self, key: object) -> object:
        _entry = self._get_entry_by(key)
        return _entry.value

    def __getitem__(self, item):
        return self._get_by(item)

    def __setitem__(self, key, value):
        if key in self.keys:
            self.remove(key)
        self.add(key, value)

    @property
    def keys(self):
        return [_entry.key for _entry in self._entries if _entry]

    @property
    def values(self):
        return [_entry.value for _entry in self._entries if _entry]

    @property
    def is_full(self):
        return self.length >= self._max_capacity

