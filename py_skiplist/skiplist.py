from math import log

import collections
from itertools import chain, takewhile, dropwhile

from iterators import geometric


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
    __slots__ = ('data', 'nxt', 'key', 'prev', 'height')

    def __init__(self, key, data, nxt, prev):
        self.key = key
        self.data = data
        self.nxt = nxt
        self.prev = prev

        for level in range(len(prev)):
            prev[level].nxt[level] = self.nxt[level].prev[level] = self

nil = _Skipnode(NIL(), None, [], [])


class Skiplist(collections.MutableMapping):
    """Class for randomized indexed skip list. The default
    distribution of node heights is geometric."""

    def __init__(self, distribution=geometric(0.5), **kwargs):

        self._max_levels = 1
        self._size = 0
        self.head = _Skipnode(None, 'HEAD', [nil] * self._max_levels, [])
        self.tail = nil
        self.tail.prev.extend([self.head] * self._max_levels)
        self.distribution = distribution

        for k, v in kwargs.iteritems():
            self[k] = v

    def __len__(self):
        return self._size

    def __str__(self):
        return 'skiplist({{{}}})'.format(
            ', '.join('{key}: {value}'.format(key=node.key, value=node.data) for node in self._level())
        )

    def __getitem__(self, key):
        """Returns item with given index"""
        return self.find_node(key).data

    def __setitem__(self, key, value):
        return self.insert(key, value)

    def __delitem__(self, key):
        self.remove(key)

    def _level(self, level=0):
        node = self.head.nxt[level]
        while node is not self.tail:
            yield node
            node = node.nxt[level]

    def __iter__(self):
        """Iterate over values in sorted order"""
        return (node.key for _, node, _ in self._level())

    def _find_update(self, key):
        update = [None] * self._max_levels
        node = self.head
        for level in reversed(range(self._max_levels)):
            while node.nxt[level].key < key:
                node = node.nxt[level]
            update[level] = node
        return update

    def _scan(self, key):
        return_value = None
        prevs = [self.head] * self._max_levels
        nexts = [self.tail] * self._max_levels
        # l = int(log(1.0 / self._p, len(self))) if self._size >= 16 else self._max_levels  # TODO: fix this shit
        for level in reversed(range(self._max_levels)):
            node = next(dropwhile(lambda node_: node_.nxt[level].key <= key, chain([self.head], self._level(level))))
            if node.key == key:
                return_value = node
            else:
                prevs[level] = node
                    # nexts[level] = node

        return return_value, prevs, nexts

    def find_node(self, key):
        """Find node with given key"""
        node, _, _ = self._scan(key)
        if node is None:
            raise KeyError('Key <{0}> not found'.format(key))
        return node

    def insert(self, key, data):
            """Inserts data into appropriate position."""

            node, update, _ = self._scan(key)

            if node:
                node.data = data
                return

            node_height = next(self.distribution) + 1  # because height should be positive non-zero
            # if node's height is greater than number of levels
            # then add new levels, if not do nothing
            update.extend([self.head for _ in range(self._max_levels, node_height)])

            self.head.nxt.extend([self.tail for _ in range(self._max_levels, node_height)])

            self.tail.prev.extend([self.head for _ in range(self._max_levels, node_height)])

            new_node = _Skipnode(key, data, [update[l].nxt[l] for l in range(len(update))], update)


            # insert node to each level <= node's height after
            # corresponding node in 'update' list

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
        return ((node.key, node.data) for node in self._level())

    def iterkeys(self):
        return (item[0] for item in self.iteritems())

    def itervalues(self):
        return (item[1] for item in self.iteritems())
