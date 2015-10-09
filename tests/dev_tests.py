from __future__ import absolute_import
import unittest

from py_skiplist.skiplist import Skiplist, NIL
from py_skiplist.skiplist import geometric
from py_skiplist.iterators import uniform


class DistributionTestCase(unittest.TestCase):
    def test_geometric(self):
        p = 0.5
        g = geometric(p)
        expected = [p**i for i in range(1, 5)]
        sample = [next(g) for _ in range(10000)]
        actual = [float(sum(1 for n in sample if n == t)) / len(sample) for t in range(10)]
        self.assertAlmostEqual(1, sum(i for i in actual), delta=0.01)
        self.assertAlmostEqual(0, sum(i - j for i, j in zip(expected, actual)), delta=0.01)


class DataStructTestCase(unittest.TestCase):
    def test_nil_always_false(self):
        self.assertFalse(NIL())


class InternalsTestCase(unittest.TestCase):

    def test_scan(self):
        sl = Skiplist(distribution=uniform(2))
        self.assertEqual((None, [sl.head], [sl.tail]), sl._scan('DoesNotExist'))

        sl = Skiplist(distribution=uniform(2))
        sl[1] = 1
        sl[3] = 3
        _, scan_res, r = sl._scan(2)
        update = sl._find_update(2)
        # self.assertEqual(scan_res, update)
        # self.assertEqual(sl._scan(1)[1], sl._find_update(1))