import unittest


class MainTestCase(unittest.TestCase):
    def test_success(self):
        result = 'OK'
        self.assertEqual(result, 'OK')
