import unittest

from skiplist import Skiplist


class SkipListTestCase(unittest.TestCase):

    def test_insert(self):
        sl = Skiplist()
        sl.insert(1, 1)
        e = sl[1]
        self.assertEqual(e, 1)

    def test_update(self):
        sl = Skiplist()
        sl['foo'] = 'bar'
        self.assertEqual(sl['foo'], 'bar')
        sl['foo'] = 'baz'
        self.assertEqual(sl['foo'], 'baz')

    def test_remove(self):
        sl = Skiplist()
        sl['what'] = 'that'
        self.assertTrue(sl['what'])
        del sl['what']
        self.assertRaises(KeyError, lambda: sl['what'])

if __name__ == '__main__':
    unittest.main()