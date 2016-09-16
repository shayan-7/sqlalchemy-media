from os.path import abspath, join, dirname, exists
from os import makedirs, remove

from sqlalchemy_media.stores.base import Store, Stream
from sqlalchemy_media.helpers import copy_stream, open_stream


class FileSystemStore(Store):

    def __init__(self, root_path: str, chunk_size: int=32768):
        self.root_path = abspath(root_path)
        self.chunk_size = chunk_size

    def _get_physical_path(self, filename: str) -> str:
        return join(self.root_path, filename)

    def put_stream(self, filename: str, stream: Stream):
        physical_path = self._get_physical_path(filename)
        physical_directory = dirname(physical_path)

        if not exists(physical_directory):
            makedirs(physical_directory, exist_ok=True)

        with open_stream(physical_path, mode='wb') as target_file:
            return copy_stream(stream, target_file, self.chunk_size)

    def delete(self, filename: str):
        remove(self._get_physical_path(filename))

    def open(self, filename: str, mode: str='rb') -> Stream:
        return open(self._get_physical_path(filename), mode=mode)