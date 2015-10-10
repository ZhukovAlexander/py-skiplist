import unittest
import collections
from py_skiplist.iterators import uniform

from py_skiplist.skiplist import Skiplist


class InterfaceTestCase(unittest.TestCase):
    def test_interface_methods_set(self):
        self.assertTrue(issubclass(Skiplist, collections.MutableMapping),
                        msg='Skiplist should alway implement the MutableMapping interface')

    def test_get(self):
        sl = Skiplist(foo='bar')
        self.assertEqual(sl.get('foo'), 'bar')
        self.assertEqual(sl.get('None', 'baz'), 'baz')
        self.assertIsNone(sl.get('Nothing'))

    def test_contains(self):
        sl = Skiplist(one=1)
        self.assertIn('one', sl)
        self.assertNotIn('two', sl)

    def test_pop(self):
        sl = Skiplist(john='Snow')
        self.assertEqual(sl.pop('john'), 'Snow')
        self.assertRaises(lambda: sl.pop('Sansa'))

    def test_iteritems(self):
        sl = Skiplist(one=1, two=2)
        self.assertListEqual(sorted([('one', 1), ('two', 2)]),
                             sorted(sl.iteritems()))


class SkipListTestCase(unittest.TestCase):

    def test_insert(self):
        sl = Skiplist()
        sl._insert(1, 1)
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
        self.assertRaises(KeyError, lambda: sl._remove('not here'))

    def test_init(self):
        sl = Skiplist(a=1, b=2)
        self.assertEqual(sl['a'], 1)
        self.assertEqual(sl['b'], 2)
        self.assertEqual(len(sl), 2)

    def test_str(self):
        sl = Skiplist()
        self.assertEqual('skiplist({})', str(sl))
        sl['1'] = 1
        self.assertEqual('skiplist({1: 1})', str(sl))

    def test_589(self):
        sl = Skiplist(distribution=uniform(2))
        sl[10] = 10
        sl[2] = 2
        sl[3] = 3
        self.assertTrue(True)

    def test_sorted(self):
        sl = Skiplist(distribution=uniform(2))
        import random
        l = [random.randint(1, 78) for i in range(10)]
        for i in l:
            sl[i] = i
        self.assertEqual(sorted(set(l)), list(sl.iterkeys()))


if __name__ == '__main__':
    unittest.main()
