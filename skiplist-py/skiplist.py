from math import log

import random


def geometric(p):
    def distribution():
        while 1:
            n = 1
            while random.randint(1, int(1 / p)) == 1:
                n += 1
            yield n
    return distribution()


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
    __slots__ = ('data', 'next', 'key')

    def __init__(self, key, data, nxt):
        self.key = key
        self.data = data
        self.next = nxt


nil = _Skipnode(NIL(), None, [])


class Skiplist(object):
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
        return 'skiplist({})'.format([node.key for node in self])

    def __getitem__(self, key):
        """Returns item with given index"""
        return self.find_node(key).data

    def __setitem__(self, key, value):
        return self.insert(key, value)

    def __delitem__(self, key):
        self.remove(key)

    def __iter__(self):
        """Iterate over values in sorted order"""
        node = self.head.next[0]
        while node is not nil:
            yield node  # .data
            node = node.next[0]

    def _find_update(self, key):
        update = [None] * self._max_levels
        node = self.head
        for level in reversed(range(self._max_levels)):
            while node.next[level].key < key:
                node = node.next[level]
            update[level] = node
        return update

    def find_node(self, key):
        """Find node with given data"""
        n = len(self)
        l = int(log(1.0 / self._p, n)) if self._size >= 16 else self._max_levels
        node = self.head
        for level in reversed(range(l)):
            while node.next[level].key <= key:
                if key == node.next[level].key:
                    return node.next[level]
                node = node.next[level]
        raise KeyError('Not found')

    def insert(self, key, data):
        """Inserts data into appropriate position."""

        try:
            self.find_node(key).data = data
        except KeyError:

            # find position to insert
            update = self._find_update(key)
            node_height = next(self.distribution)
            new_node = _Skipnode(key, data, [None] * node_height)

            # if node's height is greater than number of levels
            # then add new levels, if not do nothing
            for level in range(self._max_levels, node_height):
                update.append(self.head)
                self.head.next.append(nil)

            # insert node to each level <= node's height after
            # corresponding node in 'update' list
            for level in range(node_height):
                prev_node = update[level]
                new_node.next[level] = prev_node.next[level]
                prev_node.next[level] = new_node
            self._size += 1
            self._max_levels = max(self._max_levels, node_height)

    def remove(self, key):
        """Removes node with given data. Raises KeyError if data is not in list."""

        update = self._find_update(key)
        if key != update[0].next[0].key:
            raise KeyError

        node = update[0].next[0]
        node_height = len(node.next)
        for level in range(node_height):
            prevnode = update[level]
            prevnode.next[level] = prevnode.next[level].next[level]

        while self._max_levels > 1 and self.head.next[level] == nil:
            self._max_levels -= 1
        del node
        self._size -= 1
