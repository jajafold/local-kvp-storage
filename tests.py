import unittest
from kvp_storage import Storage
from hashlib import sha256
import os


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

    def test_saving(self):
        self.storage["2"] = 4
        self.storage["5"] = 3
        self.storage[True] = False
        self.storage[3] = "2"
        self.storage.save_to("repository/test.json")
        self.assertTrue(os.path.exists("repository/test.json"))

    def test_loading(self):
        self.storage = Storage.load_from("repository/test.json")
        self.assertEqual(self.storage["2"], 4)
        self.assertEqual(self.storage["5"], 3)
        self.assertEqual(self.storage[True], False)
        self.assertEqual(self.storage[3], "2")

    def test_overloading_rehashing(self):
        complicated_key = SimpleClass()
        self.storage = Storage(capacity=2)
        self.storage["1"] = 1
        self.storage["2"] = 2
        self.storage[complicated_key] = 3
        self.assertNotEqual(self.storage._capacity, 2)
        self.assertEqual(self.storage._capacity, 4)
        self.assertEqual(self.storage["1"], 1)
        self.assertEqual(self.storage["2"], 2)
        self.assertEqual(self.storage[complicated_key], 3)

    def test_collision(self):
        self.storage = Storage(3)
        key_one = 3
        key_two = 6
        # buckets are equal
        self.storage[key_one] = 2
        self.storage[key_two] = 5
        self.assertEqual(self.storage[key_one], 2)
        self.assertEqual(self.storage[key_two], 5)
        self.storage.remove(key_two)
        self.assertTrue(key_two not in self.storage.keys)

    def test_free(self):
        self.storage = Storage()
        complicated_key = SimpleClass()
        self.storage[complicated_key] = 2
        self.storage.remove(complicated_key)
        simple_key = "5"
        self.storage[simple_key] = 7
        self.assertEqual(self.storage[simple_key], 7)