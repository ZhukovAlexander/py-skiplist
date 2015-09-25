import unittest

from skiplist import Skiplist


class SkipListTestCase(unittest.TestCase):

    def test_insert(self):
        sl = Skiplist()
        sl.insert(1, 1)
        e = sl[1]
        self.assertEqual(e, 1)

if __name__ == '__main__':
    unittest.main()