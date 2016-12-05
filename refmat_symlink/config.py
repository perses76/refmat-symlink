import os


class Config(object):
    def __init__(self, root):
        self.root = root

    @property
    def db_path(self):
        return self.root

    @property
    def libraries_path(self):
        return os.path.join(self.db_path, 'Libraries')

    @property
    def objects_path(self):
        return os.path.join(self.db_path, 'Objects')

    @property
    def filesdb_path(self):
        return os.path.join(self.db_path, 'FilesDB')
