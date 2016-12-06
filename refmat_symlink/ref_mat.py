import os
import shutil
from datetime import datetime

now = datetime.now


class RefMat(object):
    def __init__(self, config=None, symlink_manager=None):
        self.config = config
        if not os.path.exists(config.root):
            self.reset_db()

    def reset_db(self):
        if os.path.exists(self.config.root):
            shutil.rmtree(self.config.root)
        os.makedirs(self.config.root)
        os.makedirs(self.config.libraries_path)
        os.makedirs(self.config.items_path)
        os.makedirs(self.config.repository_path)
        os.makedirs(self.config.inbox_path)

    def import_files(self, files, libraries, items, for_bakup=False, info=None):
        item_paths = []
        for fn in files:
            import_file = os.path.join(self.config.inbox_path, fn)
            item_path = self._import_file_to_repository(import_file)
            self._link_file(item_path, fn, libraries, self.config.libraries_path)
            self._link_file(item_path, fn, items, self.config.items_path)
            item_paths.append(item_path)
            if os.path.isdir(import_file):
                shutil.rmtree(import_file)
            else:
                os.remove(import_file)
        return item_paths

    def _link_file(self, item_path, filename, folders, root):
            for folder in folders:
                self.config.symlink_manager.create_symlink(
                    source=item_path,
                    target=os.path.join(
                        self._get_or_create_folder(root, folder),
                        filename
                    ),
                )

    def _import_file_to_repository(self, file_name):
        folder = self._get_today_repository_folder()
        dest = os.path.join(folder, os.path.basename(file_name))
        if os.path.isdir(file_name):
            shutil.copytree(file_name, dest)
        else:
            shutil.copy(file_name, dest)
        return dest

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

    def get_library_path(self, library):
        raise NotImplementedError()

    def get_object_path(self, object_name):
        raise NotImplementedError()

    def get_back_path(self, library):
        raise NotImplementedError()
