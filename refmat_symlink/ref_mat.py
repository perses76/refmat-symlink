import os
import stat
import shutil
from datetime import datetime

now = datetime.now


def _del_rw(action, name, exc):
    os.chmod(name, stat.S_IWRITE)
    os.remove(name)


class RefMat(object):
    def __init__(self, config=None, symlink_manager=None):
        self.config = config

    def initializedb(self):
        self._reset_db()

    def import_files(self, tags, files=None, info=None):
        self._assert_db_exists()
        item_paths = []
        if files is None:
            files = self.get_all_inbox_items()
        for fn in files:
            import_file = os.path.join(self.config.inbox_path, fn)
            item_path = self._import_file_to_repository(import_file)
            for tag in tags:
                target = os.path.join(
                    self._get_or_create_folder(self.config.tags_path, tag),
                    fn
                )
                target = self._generate_new_file_name(target)
                self.config.symlink_manager.create_symlink(
                    source=item_path,
                    target=target,
                )

            item_paths.append(item_path)
            if os.path.isdir(import_file):
                shutil.rmtree(import_file, onerror=_del_rw)
            else:
                os.remove(import_file)

        return item_paths

    def get_all_inbox_items(self):
        self._assert_db_exists()
        return [fn for fn in os.listdir(self.config.inbox_path)]

    def _assert_db_exists(self):
        if not self.is_db_initialized():
            raise ValueError('Refmat DB is not initialized')

    def _reset_db(self):
        if os.path.exists(self.config.root):
            shutil.rmtree(self.config.root, onerror=_del_rw)
        os.makedirs(self.config.root)
        os.makedirs(self.config.tags_path)
        os.makedirs(self.config.repository_path)
        os.makedirs(self.config.inbox_path)

    def is_db_initialized(self):
        return os.path.exists(self.config.root)

    def _import_file_to_repository(self, file_name):
        folder = self._get_today_repository_folder()
        dest = os.path.join(folder, os.path.basename(file_name))
        dest = self._generate_new_file_name(dest)
        if os.path.isdir(file_name):
            shutil.copytree(file_name, dest)
        else:
            shutil.copy(file_name, dest)
        return dest

    def _generate_new_file_name(self, path):
        if not os.path.exists(path):
            return path
        nm = 1
        filename, ext = os.path.splitext(path)
        while True:
            path = '{}[{}]{}'.format(filename, nm, ext)
            if not os.path.exists(path):
                return path
            nm += 1

    def _get_today_repository_folder(self):
        dt = now()
        return self._get_or_create_folder(
            self.config.repository_path,
            dt.strftime('%Y%m'),
            dt.strftime('%d'),
        )

    def _get_or_create_folder(self, *steps):
        path = ''
        for step in steps:
            path = os.path.join(path, step)
            if not os.path.exists(path):
                os.makedirs(path)
        return path
