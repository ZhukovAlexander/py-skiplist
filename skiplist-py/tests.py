import unittest
import collections

from skiplist import Skiplist, NIL
from iterators import LevelNodeIterator, AllNodesIterator, geometric

from skiplist import _Skipnode, nil


class DataStructTestCase(unittest.TestCase):
    def test_nil_always_false(self):
        self.assertFalse(NIL())


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
        self.assertRaises(KeyError, lambda: sl.remove('not here'))

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


class LevelIteratorTestCase(unittest.TestCase):
    def test_iterator_default(self):
        s = Skiplist(foo=1, bar=2)
        self.assertListEqual(sorted(['foo', 'bar']), sorted(node.key for node in LevelNodeIterator(s)))


class AllNodesIteratorTestCase(unittest.TestCase):
    def test_iterator(self):
        s = Skiplist(foo=1, bar=2)
        self.assertListEqual(sorted(['foo', 'bar']), sorted(node.key for node in AllNodesIterator(s, 1)))


class DistributionTestCase(unittest.TestCase):
    def test_geometric(self):
        g = geometric(0.5)
        expected = [0.5, 0.25, 0.125, 0.068]
        sample = [next(g) for _ in range(10000)]
        actual = [float(sum(1 for n in sample if n == t)) / len(sample) for t in [0, 1, 2, 3]]
        self.assertAlmostEqual(0, sum(i - j for i, j in zip(expected, actual)), delta=0.01)


class SkipNodeTestCase(unittest.TestCase):
    def test_iter_level(self):
        sl = Skiplist(foo='bar')
        self.assertEqual(list(sl.head.iter_level()), [sl.head, sl.head.nxt[0], sl.head.nxt[0].nxt[0]])

if __name__ == '__main__':
    unittest.main()
