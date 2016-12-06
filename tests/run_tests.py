import os
import sys
import unittest
sys.path.insert(0, os.path.abspath('..'))


PROJECT_DIR = os.path.abspath('..')


from refmat_symlink import config
import context


context.config = config.Config(os.path.join(PROJECT_DIR, '_db'))


suite = unittest.TestLoader().discover('.')
unittest.TextTestRunner().run(suite)
print('End!')
