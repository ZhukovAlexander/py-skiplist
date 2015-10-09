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
