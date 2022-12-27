from kvp_storage import Storage
import argparse
import os


def _invoke_user_commands(storage: Storage):
    while True:
        _command_str = input("> ")
        _command_args = _command_str.split()

        if _command_args[0].lower() == "exit":
            return

        elif _command_args[0].lower() == "help":
            _help_str = (
                "Available commands:\n"
                "   help\n"
                "   view\n"
                "   keys\n"
                "   values\n"
                "   add <key> <value>\n"
                "   m_add <key1>,<key2>,... <value1>,<value2>,...\n"
                "   remove <key>\n"
                "   save\n"
                "   exit\n"
            )
            print(_help_str)

        elif _command_args[0].lower() == "save":
            storage.save()
            print(f"Successfully saved to ../repository/{storage._dump_file_name}")

        elif _command_args[0].lower() == "view":
            for _entry in storage._entries:
                print(f"{_entry.key} : {_entry.value}")

        elif _command_args[0].lower() == "keys":
            print("\n".join(storage.keys))

        elif _command_args[0].lower() == "values":
            print("\n".join(storage.values))

        elif _command_args[0].lower() == "add":
            raise NotImplementedError

        elif _command_args[0].lower() == "m_add":
            raise NotImplementedError

        elif _command_args[0].lower() == "remove":
            raise NotImplementedError

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
