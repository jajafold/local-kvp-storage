from hashlib import md5
from cluster import Cluster
import os


class Manager:
    def __init__(self, repository_name: str, capacity: int = 11):
        self._repository_name = repository_name
        self._path = f'repository/{self._repository_name}'
        self._capacity = capacity

        self.__initialize()
        self._clusters = os.listdir(self._path)

    def __initialize(self):
        if not os.path.exists(f'repository/{self._repository_name}'):
            os.makedirs(f'repository/{self._repository_name}')

    def _compute_hash_and_cluster(self, key: str):
        _md5 = md5(key.encode())
        _hash = int(_md5.hexdigest(), 16) & 0x7FFFFFFF

        return _hash, _hash % self._capacity

    def _create_cluster(self, cluster_index: int) -> Cluster:
        _cluster = Cluster(self._repository_name, cluster_index)
        self._clusters.append(f'{_cluster._cluster_name}.json')

        return _cluster

    def _get_cluster_from_index(self, cluster_index) -> Cluster:
        if cluster_index not in map(Cluster.get_index_from_cluster_name, self._clusters):
            raise KeyError('Such a key does not exist in the database')

        _path = f'repository/{self._repository_name}/{self._repository_name}_{cluster_index}.json'
        _cluster = Cluster.load_from(_path)

        return _cluster

    def _search_for_free_cluster(self, current_cluster: Cluster) -> Cluster:
        while current_cluster._next != -1:
            return self._search_for_free_cluster(self._get_cluster_from_index(current_cluster._next))

        return current_cluster

    def _search_through_chain(self, current_cluster: Cluster, key: str) -> Cluster:
        while key not in current_cluster.keys:
            if current_cluster._next == -1:
                raise KeyError('Such a key does not exist in the database')

            _next = self._get_cluster_from_index(current_cluster._next)
            return self._search_through_chain(_next, key)

        return current_cluster

    def _generate_chain(self, current_cluster: Cluster) -> Cluster:
        for _cluster_name in self._clusters:
            _cluster_index = Cluster.get_index_from_cluster_name(_cluster_name)
            if current_cluster._index == _cluster_index:
                continue

            _candidate_cluster = self._get_cluster_from_index(_cluster_index)
            if not _candidate_cluster.is_full:
                current_cluster._next = _candidate_cluster._index
                return _candidate_cluster

    def multiple_add(self, keys: list, values: list):
        if len(keys) != len(values):
            raise IndexError('Lists of keys and values must be the same size')

        for key, value in zip(keys, values):
            self.add(key, value)

    def add(self, key: str, value: str):
        _, _cluster_index = self._compute_hash_and_cluster(key)
        _cluster = None
        if _cluster_index not in map(Cluster.get_index_from_cluster_name, self._clusters):
            _cluster = self._create_cluster(_cluster_index)
        else:
            _path = f'repository/{self._repository_name}/{self._repository_name}_{_cluster_index}.json'
            _cluster = Cluster.load_from(_path)

        if _cluster.is_full and _cluster._next != -1:
            _cluster = self._search_for_free_cluster(_cluster)
        elif _cluster.is_full:
            _cluster = self._generate_chain(_cluster)

        _cluster.add(key, value)

    def remove(self, key: str):
        _, _cluster_index = self._compute_hash_and_cluster(key)
        _cluster = self._get_cluster_from_index(_cluster_index)

        if _cluster._next != -1:
            _cluster = self._search_through_chain(_cluster, key)

        if not _cluster.remove(key):
            self._clusters.remove(f'{self._repository_name}_{_cluster_index}.json')

    def _get_cluster_by(self, key: str):
        _, _cluster_index = self._compute_hash_and_cluster(key)
        if _cluster_index not in map(Cluster.get_index_from_cluster_name, self._clusters):
            raise KeyError('Such a key does not exist in the database')

        _path = f'repository/{self._repository_name}/{self._repository_name}_{_cluster_index}.json'
        _cluster = Cluster.load_from(_path)
        return _cluster

    def __getitem__(self, key):
        return self._get_cluster_by(key).__getitem__(key)

    def __setitem__(self, key, value):
        self._get_cluster_by(key).__setitem__(key, value)

    @property
    def keys(self) -> str:
        for _cluster_name in self._clusters:
            _path = f'repository/{self._repository_name}/{_cluster_name}'
            _cluster = Cluster.load_from(_path)

            for _key in _cluster.keys:
                yield _key

    @property
    def values(self):
        for _cluster_name in self._clusters:
            _path = f'repository/{self._repository_name}/{_cluster_name}'
            _cluster = Cluster.load_from(_path)

            for _value in _cluster.keys:
                yield _value
