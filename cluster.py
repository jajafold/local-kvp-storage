from kvp_storage import Storage, Entry
from jsonpickle import encode, decode
import os


class Cluster:
    def __init__(self, repository_name: str, cluster_index: int):
        self._repository_name = repository_name
        self._index = cluster_index
        self._cluster_name = f'{self._repository_name}_{self._index}'
        self._path = f'repository/{self._repository_name}/{self._cluster_name}.json'
        self._storage = Storage(self._repository_name, dump_file_name=f'{self._cluster_name}_storage')
        self._next = -1

    def __save(self):
        with open(self._path, 'w') as _f:
            _f.write(encode(self, unpicklable=True, max_depth=10))

    def __delete(self):
        os.remove(self._path)

    @property
    def keys(self) -> list:
        return self._storage.keys

    @property
    def values(self) -> list:
        return self._storage.values

    @staticmethod
    def get_index_from_cluster_name(cluster_name: str) -> int:
        _start_index = cluster_name.rfind('_') + 1
        _end_index = len(cluster_name) if '.json' not in cluster_name else len(cluster_name) - 5

        return int(cluster_name[_start_index:_end_index])

    @property
    def is_full(self) -> bool:
        return self._storage.is_full

    def add(self, key: str, value: str):
        self._storage.add(key, value)
        self.__save()

    def remove(self, key: str) -> bool:
        _is_required = self._storage.remove(key)
        if not _is_required:
            self.__delete()
        else:
            self.__save()

        return _is_required

    @staticmethod
    def load_from(_path: str):
        with open(_path, 'r') as _f:
            _raw = _f.read()

        return decode(_raw, classes=[Cluster, Storage, Entry])

    def __getitem__(self, key):
        return self._storage.__getitem__(key)

    def __setitem__(self, key, value):
        self._storage.__setitem__(key, value)