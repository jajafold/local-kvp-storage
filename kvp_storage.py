from entry import Entry
from hashlib import sha256
import jsonpickle
import json
from queue import Queue


class Storage(object):
    def __init__(self):
        self._capacity = 29
        self.length = 0
        self._buckets = [-1 for _ in range(self._capacity)]
        self._entries = []
        self._free = []
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
        self._buckets[bucket] = len(self._entries)
        self.length += 1
        # TODO: Проверка на free
        self._entries.append(Entry(key=key, value=value, target_bucket=bucket, next=_old_index))

    def _search_through_chain(self, key: object, entry: Entry) -> object:
        if entry.key != key:
            return self._search_through_chain(key, self._entries[entry.next])

        return entry

    def multiple_add(self, keys: list[object], values: list[object]):
        if len(keys) != len(values):
            raise IndexError("Keys and values lists aren't the same length")

        for key, value in zip(keys, values):
            self.add(key, value)

    def add(self, key: object, value: object):
        if self.length == self._capacity:
            self._rehash()

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
            self._entries[_free_index] = Entry(key=key, value=value, target_bucket=_bucket)

    def _remove_without_chain(self, bucket):
        self._entries[self._buckets[bucket]] = None
        self._free.append(self._buckets[bucket])
        self._buckets[bucket] = -1

    def _remove_with_chain(self, bucket, target_entry):
        raise NotImplementedError

    def remove(self, key: object):
        _target_entry = self._get_entry_by(key)
        _bucket = _target_entry.bucket

        if _target_entry.next == -1:
            self._remove_without_chain(_bucket)
        else:
            self._remove_with_chain(_bucket, _target_entry)

        self.length -= 1
        pass

    def _get_entry_by(self, key: object) -> Entry:
        _hash, _bucket = self._compute_hash_and_bucket(key)
        _entry = None

        if self._buckets[_bucket] == -1:
            raise KeyError("Key not found")

        _entry = self._entries[self._buckets[_bucket]]
        if _entry.next != -1:
            _entry = self._search_through_chain(key, _entry)

        return _entry

    def get_by(self, key: object) -> object:
        _entry = self._get_entry_by(key)
        return _entry.value

    def save_to(self, filename):
        with open(filename, 'w') as f:
            f.write(jsonpickle.encode(self, unpicklable=False))

    @staticmethod
    def load_from(filename):
        with open(filename, 'r') as f:
            raw_json = f.read()
        result_str = jsonpickle.loads(raw_json, classes=[Storage, Entry, json.encoder.JSONEncoder])
        return Storage._get_storage_from_string(result_str)

    @staticmethod
    def _get_storage_from_string(json_string):
        result = Storage()
        result._capacity = json_string['_capacity']
        result.length = json_string['length']
        result._buckets = json_string['_buckets']
        result._entries = list(map(Entry.get_entry_by_string, json_string['_entries']))
        result._free = json_string['_free']
        return result

    @property
    def keys(self):
        return [_entry.key for _entry in self._entries if _entry]

    @property
    def values(self):
        return [_entry.value for _entry in self._entries if _entry]




