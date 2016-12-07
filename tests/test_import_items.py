import os
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

        self.tags = None
        self.files = None
        self.today_datetime = datetime(2015, 6, 1, 18, 45, 23)

        self.expeted_repository_path = None
        self.expected_files = None

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

    def assert_files_does_not_exists_in_inbox(self):
        for file_name in self.expected_files:
            self.assert_file_not_exists(self.config.inbox_path, file_name)

    def assert_files_exists_in_tags(self):
        for tag in self.tags:
            for file_name in self.expected_files:
                self.assert_file_exists(self.config.tags_path, tag, file_name)

    def assert_files_in_repository_exist(self):
        for file_name in self.expected_files:
            self.assert_file_exists(self.config.repository_path, self.expeted_repository_path, file_name)

    def assert_file_exists(self, *path):
        full_path = os.path.join(self.config.root, *path)
        self.assertTrue(os.path.exists(full_path), 'File does not exists: {}'.format(full_path))

    def assert_file_not_exists(self, *path):
        full_path = os.path.join(self.config.root, *path)
        self.assertFalse(os.path.exists(full_path), 'File exists: {}'.format(full_path))

    def create_item_in_inbox(self, item_name):
        with open(os.path.join(self.config.inbox_path, item_name), 'w+') as f:
            f.write('file_content')

    def test_import_file(self):
        test_filename = 'test.txt'
        self.create_item_in_inbox(test_filename)
        self.today_datetime = datetime(2014, 6, 1, 18, 45, 23)

        self.files = [test_filename]
        self.tags = [
            os.path.join('libs', 'mylib'),
            os.path.join('subjects', 'mysubj')
        ]

        self.call_target()

        self.assert_files_in_repository_exist()
        self.assert_files_exists_in_tags()
        self.assert_files_does_not_exists_in_inbox()

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
