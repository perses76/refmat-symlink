class RefMat(object):
    def __init__(self, config=None, symlink_manager=None):
        self.config = config
        self.symlink = symlink_manager

    def import_items(self, items, libraries, objects, for_bakup=False, info=None):
        item_path = self.copy_item_to_filedb(items)
        library_path = self.get_library_path(libraries)
        self.symlink.create(item_path, library_path)
        object_path = self.get_object_path(objects)
        self.symlink.create(item_path, object_path)
        backup_path = self.get_backup_path()
        self.symlink.create(item_path, backup_path)
        return item_path

    def get_library_path(self, library):
        raise NotImplementedError()

    def get_object_path(self, object_name):
        raise NotImplementedError()

    def get_back_path(self, library):
        raise NotImplementedError()
