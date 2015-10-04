from math import log

import collections
from itertools import chain

from iterators import LevelNodeIterator, AllNodesIterator, geometric


class NIL(object):
    """Sentinel object that always compares greater than another object"""
    __slots__ = ()

    def __cmp__(self, other):
        return 1

    def __str__(self):
        return 'NIL'

    def __nonzero__(self):
        return False


class _Skipnode(object):
    __slots__ = ('data', 'nxt', 'key')

    def __init__(self, key, data, nxt):
        self.key = key
        self.data = data
        self.nxt = nxt

    def iter_level(self, level=0):
        return chain([self], self.nxt[level].iter_level() if self.nxt and self.nxt[level] else [])


nil = _Skipnode(NIL(), None, [])


class Skiplist(collections.MutableMapping):
    """Class for randomized indexed skip list. The default
    distribution of node heights is geometric."""

    def __init__(self, p=0.5, distribution=geometric, **kwargs):

        self._p = p
        self._max_levels = 1
        self._size = 0
        self.head = _Skipnode(None, 'HEAD', [nil] * self._max_levels)
        self.distribution = distribution(p)

        for k, v in kwargs.iteritems():
            self[k] = v

    def __len__(self):
        return self._size

    def __str__(self):
        return 'skiplist({{{}}})'.format(
            ','.join('{key}: {value}'.format(key=node.key, value=node.data) for node in LevelNodeIterator(self))
        )

    def __getitem__(self, key):
        """Returns item with given index"""
        return self.find_node(key).data

    def __setitem__(self, key, value):
        return self.insert(key, value)

    def __delitem__(self, key):
        self.remove(key)

    def _iter_level(self, level=0):
        return self.head.iter_level(level)

    def __iter__(self):
        """Iterate over values in sorted order"""
        return (node.key for node in self._iter_level())

    def _find_update(self, key):
        update = [None] * self._max_levels
        node = self.head
        for level in reversed(range(self._max_levels)):
            # for node in LevelNodeIterator(self, level):
            #     if node.nxt[level].key >= key:
            #         update[level] = node
            #         break
            while node.nxt[level].key < key:
                node = node.nxt[level]
            update[level] = node
        return update

    def find_node(self, key):
        """Find node with given key"""
        l = int(log(1.0 / self._p, len(self))) if self._size >= 16 else self._max_levels
        for node in AllNodesIterator(self, l):
            if node.key == key:
                return node
        raise KeyError('Key <{o}> not found'.format(key))

    def insert(self, key, data):
        """Inserts data into appropriate position."""

        try:
            self.find_node(key).data = data
        except KeyError:

            # find position to insert
            update = self._find_update(key)
            node_height = next(self.distribution) + 1  # because height should be positive non-zero
            new_node = _Skipnode(key, data, [None] * node_height)

            # if node's height is greater than number of levels
            # then add new levels, if not do nothing
            for level in range(self._max_levels, node_height):
                update.append(self.head)
                self.head.nxt.append(nil)

            # insert node to each level <= node's height after
            # corresponding node in 'update' list
            for level in range(node_height):
                prev_node = update[level]
                new_node.nxt[level] = prev_node.nxt[level]
                prev_node.nxt[level] = new_node
            self._size += 1
            self._max_levels = max(self._max_levels, node_height)

    def remove(self, key):
        """Removes node with given data. Raises KeyError if data is not in list."""

        update = self._find_update(key)
        if key != update[0].nxt[0].key:
            raise KeyError

        node = update[0].nxt[0]
        node_height = len(node.nxt)
        for level in range(node_height):
            prevnode = update[level]
            prevnode.nxt[level] = prevnode.nxt[level].nxt[level]

        while self._max_levels > 1 and self.head.nxt[level] == nil:
            self._max_levels -= 1
        del node
        self._size -= 1

    def iteritems(self):
        return ((node.key, node.data) for node in LevelNodeIterator(self))

    def iterkeys(self):
        return (item[0] for item in self.iteritems())

    def itervalues(self):
        return (item[1] for item in self.iteritems())
