from kvp_storage import Storage


class Simple_class:
    def __init__(self):
        self.numeric = 123
        self.string = "abc"
        self.simple_array = [1, 2, self.numeric, self.string]


if __name__ == "__main__":
    _kvp = Storage()
    _simple = Simple_class()
    keys = ["key_mul_1", "key_mul_2", "key_mul_3"]
    values = ["value_mul_1", "value_mul_2", "value_mul_3"]

    _kvp.add("1", 2)
    _kvp.add("key_abc", "value_123")
    _kvp.add("key_array", [1, 2, 3])
    _kvp.add("key_simple", _simple)
    _kvp.multiple_add(keys, values)

    print("--------------BEFORE--------------")
    for entry in _kvp._entries:
        print(f"B[{entry._bucket}] -> {entry.value} | NEXT: {entry._next}")

    _kvp.remove("key_array")
    print()
    print("--------------AFTER--------------")
    for entry in _kvp._entries:
        if not entry:
            continue
        print(f"B[{entry._bucket}] -> {entry.value} | NEXT: {entry._next}")
