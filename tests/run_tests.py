import os
import sys
import unittest
import shutil
sys.path.insert(0, os.path.abspath('..'))


PROJECT_DIR = os.path.abspath('..')


from refmat_symlink import config
from refmat_symlink.ref_mat import RefMat
import context


def create_refmat(config):
    if os.path.exists(config.db_path):
        shutil.rmtree(config.db_path)
    os.makedirs(config.db_path)
    os.makedirs(config.libraries_path)
    os.makedirs(config.objects_path)
    os.makedirs(config.filesdb_path)
    ref_mat = RefMat(config=config)
    return ref_mat


context.ref_mat = create_refmat(config.Config(os.path.join(PROJECT_DIR, '_db')))


suite = unittest.TestLoader().discover('.')
unittest.TextTestRunner().run(suite)
print('End!')
