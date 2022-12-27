from kvp_storage import Storage

if __name__ == "__main__":
    _kvp = Storage()
    keys = ["key_mul_1", "key_mul_2", "key_mul_3"]
    values = ["value_mul_1", "value_mul_2", "value_mul_3"]

    _kvp["1"] = 2
    _kvp["key_abc"] = "value_123"
    _kvp["key_array"] = [1, 2, 3]
    _kvp.multiple_add(keys, values)

    _kvp.save()
