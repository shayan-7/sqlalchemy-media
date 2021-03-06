import unittest
import io
from os import makedirs
from os.path import join, dirname, abspath, exists, getsize

from sqlalchemy_media.stores import FileSystemStore


class FileSystemStoreTestCase(unittest.TestCase):

    def setUp(self):
        self.this_dir = abspath(dirname(__file__))
        self.base_url = 'http://static1.example.orm'
        self.stuff_path = join(self.this_dir, 'stuff')
        self.sample_text_file1 = join(self.stuff_path, 'sample_text_file1.txt')
        self.temp_path = join(self.this_dir, 'temp', 'test_filesystem_store')
        if not exists(self.temp_path):  # pragma: no cover
            makedirs(self.temp_path, exist_ok=True)

    def test_put_from_stream(self):
        store = FileSystemStore(self.temp_path, self.base_url)
        target_filename = 'test_put_from_stream/file_from_stream1.txt'
        content = b'Lorem ipsum dolor sit amet'
        stream = io.BytesIO(content)
        length = store.put(target_filename, stream)
        self.assertEqual(length, len(content))
        self.assertTrue(exists(join(self.temp_path, target_filename)))

    def test_delete(self):

        store = FileSystemStore(self.temp_path, self.base_url)
        target_filename = 'test_delete/sample_text_file1.txt'
        with open(self.sample_text_file1, 'rb') as f:
            length = store.put(target_filename, f)
        self.assertEqual(length, getsize(self.sample_text_file1))
        self.assertTrue(exists(join(self.temp_path, target_filename)))

        store.delete(target_filename)
        self.assertFalse(exists(join(self.temp_path, target_filename)))

    def test_open(self):
        store = FileSystemStore(self.temp_path, self.base_url)
        target_filename = 'test_open/sample_text_file1.txt'
        with open(self.sample_text_file1, 'rb') as f:
            length = store.put(target_filename, f)
        self.assertEqual(length, getsize(self.sample_text_file1))
        self.assertTrue(exists(join(self.temp_path, target_filename)))

        # Reading
        with store.open(target_filename, mode='rb') as stored_file, \
                open(self.sample_text_file1, mode='rb') as original_file:
            self.assertEqual(stored_file.read(), original_file.read())

        # Writing
        new_content = b'Some Binary Data'
        with store.open(target_filename, mode='wb') as stored_file:
            stored_file.write(new_content)

        with store.open(target_filename, mode='rb') as stored_file:
            self.assertEqual(stored_file.read(), new_content)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
