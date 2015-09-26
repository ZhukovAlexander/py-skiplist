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

    def test_init(self):
        sl = Skiplist(a=1, b=2)
        self.assertEqual(sl['a'], 1)
        self.assertEqual(sl['b'], 2)
        self.assertEqual(len(sl), 2)

    def test_str(self):
        sl = Skiplist()
        self.assertEqual('skiplist([])', str(sl))
        sl['1'] = 1
        self.assertEqual('skiplist([\'1\'])', str(sl))
if __name__ == '__main__':
    unittest.main()