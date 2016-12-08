import os
import random
import unittest
from unittest import mock
from datetime import datetime
from refmat_symlink.ref_mat import RefMat
from refmat_symlink import config


SOLUTION_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


class MainTestCase(unittest.TestCase):

    def setUp(self):
        self.config = config.Config(os.path.join(SOLUTION_DIR, '_db'))
        self.ref_mat = RefMat(config=self.config)
        self.ref_mat.initializedb()

        self.tags = [os.path.join('libs', 'mylib')]
        self.files = []
        self.today_datetime = datetime(2015, 6, 1, 18, 45, 23)

        self.expeted_repository_path = None
        self.expected_files = None
        self.expected_tags = None

    def assert_result(self):
        self.assert_files_in_repository_exist()
        self.assert_files_exists_in_tags()
        self.assert_files_does_not_exists_in_inbox()

    def call_target(self):
        with mock.patch('refmat_symlink.ref_mat.now') as m:
            m.return_value = self.today_datetime
            self.ref_mat.import_files(
                files=self.files,
                tags=self.tags
            )
            self.expeted_repository_path = os.path.join(self.today_datetime.strftime('%Y%m'), self.today_datetime.strftime('%d'))
            if self.expected_files is None:
                self.expected_files = self.files

            if self.expected_tags is None:
                self.expected_tags = [
                    os.path.join(tag, fn)
                    for tag in self.tags
                    for fn in self.expected_files
                ]

    def assert_files_does_not_exists_in_inbox(self):
        for file_name in self.expected_files:
            self.assert_file_not_exists(self.config.inbox_path, file_name)

    def assert_files_exists_in_tags(self):
        for file_name in self.expected_tags:
            self.assert_file_exists(self.config.tags_path, file_name)

    def assert_files_in_repository_exist(self):
        for file_name in self.expected_files:
            self.assert_file_exists(self.config.repository_path, self.expeted_repository_path, file_name)

    def assert_file_exists(self, *path):
        full_path = os.path.join(self.config.root, *path)
        self.assertTrue(os.path.exists(full_path), 'File does not exists: {}'.format(full_path))

    def assert_file_not_exists(self, *path):
        full_path = os.path.join(self.config.root, *path)
        self.assertFalse(os.path.exists(full_path), 'File exists: {}'.format(full_path))

    def _get_random_name(self, num=8):
        return ''.join([random.choice('qwertyuiopasdfghjklzxcvbnm1234567890') for idx in range(num)])

    def _create_item(self, *path):
        with open(os.path.join(*path), 'w+') as f:
            f.write('file_content')

    def create_item_in_inbox(self, item_name=None):
        if item_name is None:
            item_name = self._get_random_name()
        self._create_item(self.config.inbox_path, item_name)
        self.files.append(item_name)
        return item_name

    def create_item_in_repository(self):
        item_name = self._get_random_name()
        self._create_item(self.config.repository_path, item_name)
        self.files.append(item_name)
        return item_name

    def test_default(self):
        self.call_target()
        self.assert_result()

    def test_import_file_success(self):
        file_name = self.create_item_in_inbox()

        self.today_datetime = datetime(2014, 6, 1, 18, 45, 23)
        self.expeted_repository_path = os.path.join('201406', '01')

        self.files = [file_name]
        self.expected_files = [file_name]

        self.tags = [os.path.join('libs', 'mylib')]
        self.expected_tags = [os.path.join('libs', 'mylib')]

        self.call_target()
        self.assert_result()

    def test_folder_already_exists(self):
        pass

    def test_import_folder(self):
        test_foldername = 'test.txt'
        os.makedirs(os.path.join(self.config.inbox_path, test_foldername))

        self.files = [test_foldername]
        self.tags = [
            os.path.join('libs', 'mylib'),
            os.path.join('subjects', 'mysubj')
        ]
        self.call_target()

        self.assert_files_in_repository_exist()
        self.assert_files_exists_in_tags()
        self.assert_files_does_not_exists_in_inbox()

    def test_import_all_items(self):
        self.expected_files = ['test1.txt', 'test2.txt']
        for fn in self.expected_files:
            self.create_item_in_inbox(fn)

        self.files = None
        self.tags = [
            os.path.join('libs', 'mylib'),
            os.path.join('subjects', 'mysubj')
        ]

        self.call_target()
        self.assert_result()

    def test_import_file_with_same_name(self):
        test_filename = 'test.txt'
        self.create_item_in_inbox(test_filename)
        self.files = [test_filename]
        self.tags = [
            os.path.join('libs', 'mylib'),
        ]

        self.call_target()
        # create item and import files again
        self.create_item_in_inbox(test_filename)
        self.files = [test_filename]
        self.call_target()
        self.expected_files = [
            test_filename,
            'test[1].txt'
        ]
        self.expected_tags = [
            os.path.join('libs', 'mylib', test_filename),
            os.path.join('libs', 'mylib', 'test[1].txt'),
        ]

        self.assert_result()

    def test_import_folder_with_same_name(self):
        test_foldername = 'testtxt'
        os.makedirs(os.path.join(self.config.inbox_path, test_foldername))
        self.files = [test_foldername]
        self.tags = [
            os.path.join('libs', 'mylib'),
        ]

        self.call_target()
        # create item and import files again
        os.makedirs(os.path.join(self.config.inbox_path, test_foldername))
        self.call_target()
        self.expected_files = [
            test_foldername,
            'testtxt[1]'
        ]
        self.expected_tags = [
            os.path.join('libs', 'mylib', test_foldername),
            os.path.join('libs', 'mylib', 'testtxt[1]'),
        ]

        self.assert_result()
