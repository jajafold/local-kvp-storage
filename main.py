from kvp_storage import Storage


class Simple_class:
    def __init__(self):
        self.numeric = 123
        self.string = "abc"
        self.simple_array = [1, 2, self.numeric, self.string]


if __name__ == "__main__":
    _kvp = Storage()
    _simple = Simple_class()

    _kvp.add(1, 2)
    _kvp.add("key_abc", "value_123")
    _kvp.add("key_abce", "value_maybe_collision")
    _kvp.add("key_array", [1, 2, 3])
    _kvp.add("key_simple", _simple)

    for entry in _kvp._entries:
        print(f"B[{entry._bucket}] -> {entry.value} | NEXT: {entry._next}")
