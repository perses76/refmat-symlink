import os
import sys
import unittest

SOLUTION_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
PROJECT_DIR = os.path.join(SOLUTION_DIR, 'refmat_symlink')
TESTS_DIR = os.path.join(SOLUTION_DIR, 'tests')

sys.path.insert(0, SOLUTION_DIR)
sys.path.insert(0, PROJECT_DIR)


suite = unittest.TestLoader().discover(TESTS_DIR)
unittest.TextTestRunner().run(suite)
print('End!')
