import os
import unittest
from unittest import mock
from datetime import datetime
import context
from refmat_symlink.ref_mat import RefMat


class MainTestCase(unittest.TestCase):

    def setUp(self):
        self.ref_mat = RefMat(config=context.config)
        self.ref_mat.reset_db()

    def assert_file_exists(self, path):
        self.assertTrue(
            os.path.exists(os.path.join(self.config.root, path)),
            'File does not exists: {}'.format(os.path.join(self.config.root, path))
        )

    def assert_file_not_exists(self, path):
        self.assertFalse(
            os.path.exists(os.path.join(self.config.root, path))
        )

    @mock.patch('refmat_symlink.ref_mat.now')
    def test_import_file(self, now_mock):
        ref_mat = self.ref_mat
        self.config = ref_mat.config
        test_filename = 'test.txt'
        test_filecontent = 'my test'
        library_name = 'mylib'
        item_name = 'myittem'
        with open(os.path.join(ref_mat.config.inbox_path, test_filename), 'w+') as f:
            f.write(test_filecontent)
        today_datetime = datetime(2015, 6, 1, 18, 45, 23)
        now_mock.return_value = today_datetime

        ref_mat.import_files(
            files=[test_filename],
            libraries=[library_name],
            items=[item_name]
        )
        self.assert_file_exists(os.path.join(self.config.repository_path, '201506', '01', test_filename))
        self.assert_file_exists(os.path.join(ref_mat.config.libraries_path, library_name, test_filename))
        self.assert_file_exists(os.path.join(ref_mat.config.items_path, item_name, test_filename))
        self.assert_file_not_exists(os.path.join(ref_mat.config.inbox_path, test_filename))

    @mock.patch('refmat_symlink.ref_mat.now')
    def test_import_folder(self, now_mock):
        ref_mat = self.ref_mat
        self.config = ref_mat.config
        test_foldername = 'test.txt'
        library_name = 'mylib'
        item_name = 'myittem'
        os.makedirs(os.path.join(ref_mat.config.inbox_path, test_foldername))
        today_datetime = datetime(2015, 6, 1, 18, 45, 23)
        now_mock.return_value = today_datetime

        ref_mat.import_files(
            files=[test_foldername],
            libraries=[library_name],
            items=[item_name]
        )
        self.assert_file_exists(os.path.join(self.config.repository_path, '201506', '01', test_foldername))
        self.assert_file_exists(os.path.join(ref_mat.config.libraries_path, library_name, test_foldername))
        self.assert_file_exists(os.path.join(ref_mat.config.items_path, item_name, test_foldername))
        self.assert_file_not_exists(os.path.join(ref_mat.config.inbox_path, test_foldername))
