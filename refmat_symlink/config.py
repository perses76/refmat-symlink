import os
from symlink_manager import SymlinkManager


class Config(object):
    def __init__(self, root, symlink_manager=None):
        self.__root = root
        self.__symling_manager = symlink_manager

    @property
    def root(self):
        return self.__root

    @property
    def symlink_manager(self):
        if self.__symling_manager is None:
            self.__symling_manager = SymlinkManager()
        return self.__symling_manager

    @property
    def tags_path(self):
        return os.path.join(self.root, 'Tags')

    @property
    def repository_path(self):
        return os.path.join(self.root, 'Repo')

    @property
    def inbox_path(self):
        return os.path.join(self.root, 'Inbox')
