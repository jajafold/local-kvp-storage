from kvp_storage import Storage
from hashlib import md5
import os


class Manager:
    def __init__(self, cluster_name: str, capacity: int = 11):
        self._cluster_name = cluster_name
        self._path = f'repository/{self._cluster_name}'
        self._capacity = capacity
        self._clusters = [None for _ in range(self._capacity)]

        self.__initialize()

    def __initialize(self):
        if not os.path.exists(f'repository/{self._cluster_name}'):
            os.makedirs(f'repository/{self._cluster_name}')

    def __clear(self):
        self._clusters = [None for _ in range(self._capacity)]

    def _compute_hash_and_cluster(self, key: str):
        _md5 = md5(key.encode())
        _hash = int(_md5.hexdigest(), 16) & 0x7FFFFFFF

        return _hash, _hash % self._capacity

    @staticmethod
    def __load_cluster_immediately(path: str) -> Storage:
        print("Cluster loaded immediately")
        return Storage.load_from(path)

    def _load_cluster(self, cluster_index: int, file_path: str):
        self._clusters[cluster_index] = Storage.load_from(file_path)
        print("Cluster loaded into memory")

    def _create_cluster(self, cluster_index: int):
        if os.path.exists(f"/repository/{self._cluster_name}/{self._cluster_name}_{cluster_index}.json"):
            self._load_cluster(cluster_index, f"/repository/{self._cluster_name}/{self._cluster_name}_{cluster_index}.json")
            return

        self._clusters[cluster_index] = Storage(
                cluster_name=self._cluster_name,
                dump_file_name=f'{self._cluster_name}_{cluster_index}')
        print("Cluster created")

    def add(self, key: str, value: str):
        _, _cluster = self._compute_hash_and_cluster(key)
        if not self._clusters[_cluster]:
            self._create_cluster(_cluster)

        self._clusters[_cluster].add(key, value)
        self.save()

    def remove(self, key: str):
        _, _cluster = self._compute_hash_and_cluster(key)
        _path = f'repository/{self._cluster_name}/{self._cluster_name}_{_cluster}.json'

        if self._clusters[_cluster] is None and not os.path.exists(_path):
            raise KeyError("Cluster was not created")
        elif self._clusters[_cluster] is None and os.path.exists(_path):
            self._load_cluster(_cluster, _path)

        self._clusters[_cluster].remove(key)
        self.save()

    def save(self):
        for _cluster in self._clusters:
            if _cluster is None:
                continue
            _cluster.save()

        self.__clear()

    def _get_cluster_by(self, key: str):
        _, _cluster = self._compute_hash_and_cluster(key)
        _path = f'repository/{self._cluster_name}/{self._cluster_name}_{_cluster}.json'

        if self._clusters[_cluster] is None and not os.path.exists(_path):
            raise KeyError("Cluster was not created")
        elif self._clusters[_cluster] is None and os.path.exists(_path):
            self._load_cluster(_cluster, _path)

        return self._clusters[_cluster]

    def __getitem__(self, key):
        return self._get_cluster_by(key).__getitem__(key)

    def __setitem__(self, key, value):
        self._get_cluster_by(key).__setitem__(key, value)

    @property
    def keys(self) -> str:
        _clusters = os.listdir(self._path)
        # for _storage in self._clusters:
        #     if _storage is None:
        #         continue
        #     for _key in _storage.keys:
        #         yield _key

        for _cluster in _clusters:
            for _key in Manager.__load_cluster_immediately(f'{self._path}/{_cluster}').keys:
                yield _key

    @property
    def values(self):
        _clusters = os.listdir(self._path)
        # for _storage in self._clusters:
        #     if _storage is None:
        #         continue
        #     for _value in _storage.values:
        #         yield _value

        for _cluster in _clusters:
            for _value in Manager.__load_cluster_immediately(f'{self._path}/{_cluster}').values:
                yield _value
