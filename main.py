from kvp_storage import Storage
import argparse
import os


def _invoke_user_commands(storage: Storage):
    while True:
        _command_str = input("> ")
        _command_args = _command_str.split()
        if not _command_args:
            continue
        _command_type = _command_args[0].lower()

        if _command_type == "exit":
            return

        elif _command_args[0].lower() == "help":
            _help_str = (
                "Available commands:\n"
                "   help\n"
                "   view\n"
                "   keys\n"
                "   values\n"
                "   get <key>\n"
                "   add <key> <value>\n"
                "   m_add <key1>,<key2>,... <value1>,<value2>,...\n"
                "   remove <key>\n"
                "   save\n"
                "   exit\n"
            )
            print(_help_str)

        elif _command_type == "save":
            storage.save()
            print(f"Successfully saved to ../repository/{storage._dump_file_name}")

        elif _command_type == "view":
            for key in storage.keys:
                print(f"{key} : {storage[key]}")

        elif _command_type == "keys":
            print("\n".join(storage.keys))

        elif _command_type == "values":
            print("\n".join(storage.values))

        elif _command_type == "add":
            if len(_command_args) != 3:
                print("Wrong usage")
                continue
            storage[_command_args[1]] = _command_args[2]
            print(f"Successfully added as {_command_args[1]}:{_command_args[2]}")

        elif _command_type == "get":
            if len(_command_args) != 2:
                print("Wrong usage")
                continue
            print(storage[_command_args[1]])

        elif _command_type == "m_add":
            if len(_command_args) != 3:
                print("Wrong usage")
                continue
            keys = _command_args[1].split(',')
            values = _command_args[2].split(',')
            storage.multiple_add(keys, values)
            print(f"Successfully added keys {keys} with values {values}")

        elif _command_type == "remove":
            if len(_command_args) != 2:
                print("Wrong usage")
            key = _command_args[1]
            storage.remove(key)
            print(f"Successfully removed key {key}")

        else:
            print("Unknown command")


if __name__ == "__main__":
    _parser = argparse.ArgumentParser(
        description="Local KVP storage", formatter_class=argparse.RawDescriptionHelpFormatter)
    _parser.add_argument(dest="dump_file_name", help="Name of the storage dump file in the ../repository/")

    _args = _parser.parse_args()
    _file_name = _args.dump_file_name
    _storage = None

    if not os.path.exists(f"repository/{_file_name}.json"):
        _storage = Storage(dump_file_name=_file_name)
        _storage.save()
        print(f"CREATED {_file_name}.json")
    else:
        _storage = Storage.load_from(f"repository/{_file_name}.json")
        print(f"LOADED {_file_name}.json")

    _invoke_user_commands(_storage)
