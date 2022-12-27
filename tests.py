import unittest
from kvp_storage import Storage
from hashlib import sha256


class SimpleClass:
    def __init__(self):
        self.numeric = 123
        self.string = "abc"
        self.simple_array = [1, 2, self.numeric, self.string]


class StorageTests(unittest.TestCase):
    def setUp(self) -> None:
        self.storage = Storage()

    def test_simple_add(self):
        self.storage.add("1", "1")
        self.assertEqual("1", self.storage["1"])

    def test_multiple_add(self):
        keys = ["1", "2"]
        values = ["1", "2"]
        self.storage.multiple_add(keys, values)
        self.assertEqual("1", self.storage["1"])
        self.assertEqual("2", self.storage["2"])

    def test_remove(self):
        self.storage["1"] = "1"
        self.storage.remove("1")
        self.assertTrue("1" not in self.storage.keys)

    def test_complicated_key(self):
        complicated_key = SimpleClass()
        self.storage[complicated_key] = 5
        self.assertTrue(complicated_key in self.storage.keys)
        self.assertEqual(5, self.storage[complicated_key])

    def test_complicated_value(self):
        complicated_value = SimpleClass()
        self.storage[2] = complicated_value
        self.assertTrue(complicated_value in self.storage.values)
        self.assertEqual(complicated_value, self.storage[2])

    def test_computing_hash_bucket(self):
        simple_key = "1"
        complicated_key = SimpleClass()
        hash_value, bucket = self.storage._compute_hash_and_bucket(simple_key)
        _sha256 = sha256(Storage._encode_object(simple_key))
        self.assertEqual(hash_value, int(_sha256.hexdigest(), 16) & 0x7FFFFFFF)

        hash_value, bucket = self.storage._compute_hash_and_bucket(complicated_key)
        _sha256 = sha256(Storage._encode_object(complicated_key))
        self.assertEqual(hash_value, int(_sha256.hexdigest(), 16) & 0x7FFFFFFF)
