from cluster_manager import Manager
import argparse
import os


def _invoke_user_commands(cluster_manager: Manager):
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
                "   clusters\n"
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
            cluster_manager.save()
            print(f"Successfully saved to ../repository/{cluster_manager._repository_name}")

        elif _command_type == "view":
            for key in cluster_manager.keys:
                print(f"{key} : {cluster_manager[key]}")

        elif _command_type == "clusters":
            if len(_command_args) != 1:
                print("Wrong usage")
                continue

            for _file in os.listdir(f'repository/{cluster_manager._repository_name}'):
                print(f'  * {_file}')

        elif _command_type == "keys":
            print("\n".join(cluster_manager.keys))

        elif _command_type == "values":
            print("\n".join(cluster_manager.values))

        elif _command_type == "add":
            if len(_command_args) != 3:
                print("Wrong usage")
                continue
            cluster_manager.add(_command_args[1], _command_args[2])
            # cluster_manager[_command_args[1]] = _command_args[2]
            print(f"Successfully added as {_command_args[1]}:{_command_args[2]}")

        elif _command_type == "get":
            if len(_command_args) != 2:
                print("Wrong usage")
                continue
            print(cluster_manager[_command_args[1]])

        elif _command_type == "m_add":
            if len(_command_args) != 3:
                print("Wrong usage")
                continue

            keys = _command_args[1].split(',')
            values = _command_args[2].split(',')
            cluster_manager.multiple_add(keys, values)
            print(f"Successfully added keys {keys} with values {values}")

        elif _command_type == "remove":
            if len(_command_args) != 2:
                print("Wrong usage")
                continue

            key = _command_args[1]
            cluster_manager.remove(key)
            print(f"Successfully removed key {key}")

        else:
            print("Unknown command")


if __name__ == "__main__":
    _parser = argparse.ArgumentParser(
        description="Local KVP storage", formatter_class=argparse.RawDescriptionHelpFormatter)
    _parser.add_argument(dest="dump_cluster_name", help="Name of the storage dump file in the ../repository/")

    _args = _parser.parse_args()
    _cluster_name = _args.dump_cluster_name
    _cluster_manager = None

    if not os.path.exists(f"repository/{_cluster_name}"):
        _cluster_manager = Manager(_cluster_name)
        print(f"CREATED {_cluster_name} cluster")
    else:
        _cluster_manager = Manager(_cluster_name)
        print(f"LOADED {_cluster_name} cluster")

    _invoke_user_commands(_cluster_manager)
