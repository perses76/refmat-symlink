import os


class SymlinkManager(object):
    def create_symlink(self, source, target):
        os.symlink(source, target)
