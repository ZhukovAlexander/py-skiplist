"""Dat skiplist"""

from numpy.random import geometric
from math import log

class NIL(object):
    'Sentinel object that always compares greater than another object'
    def __cmp__(self, other):
        return 1

    def __str__(self):
        return 'NIL'

class skipnode(object):

    def __init__(self, data, next, width):
        self.data = data
        self.next = next
        self.width = width
        
nil = skipnode(NIL(), [], [])
        
class skiplist:

    """Class for randomized indexed skip list. The default
    distribution of node heights is geometric."""

    def __init__(self, p = 0.5, distribution = geometric):

        self._p = p
        self._max_levels = 1
        self._size = 0
        
        self.head = skipnode('HEAD',[nil]*self._max_levels,[1]*self._max_levels)
        self.distribution = distribution
        
    def __len__(self):
        return self._size
    
    def __str__(self):
        s = map(str, [node.data
                      for node in self])
        return '->'.join(s)
        
    def __getitem__(self, i):
        '''Returns item with given index'''
        node = self.head
        i += 1
        for level in reversed(range(self._max_levels)):
            while node.width[level] <= i:
                i -= node.width[level]
                node = node.next[level]
        return node.data
    
    def __iter__(self):
        'Iterate over values in sorted order'
        node = self.head.next[0]
        while node is not nil:
            yield node#.data
            node = node.next[0]
        
    def find(self, data):
        '''Find node with given data'''
        n = len(self)
        L=int(log(1.0/self._p, n)) if self._size>=16 else self._max_levels
        node = self.head
        for level in reversed(range(L)):
            node = self.head.next[level]
            while node is not nil:
                if node.data > data:    break
                elif data == node.data: return node.data
                node = node.next[level]

    def insert(self, data):
        '''Inserts data into appropriate position.'''
        update = [None]*self._max_levels
        steps_at_level = [0]*self._max_levels
        node = self.head
        #find position to insert
        for level in reversed(range(self._max_levels)):
            while node.next[level].data <= data:
                steps_at_level[level] += node.width[level]
                node = node.next[level]
            update[level] = node
        node_height = self.distribution(self._p)
        newnode = skipnode(data, [None]*node_height, [0]*node_height)
        steps = 0
        #if node's height is greater than number of levels
        #then add new levels, if not do nothing
        for level in range(self._max_levels, node_height):
            update.append(self.head)
            self.head.width.append(len(self)+1)
            self.head.next.append(nil)
            steps_at_level.append(0)
            #update[level].width[level] += 1
        #insert node to each level <= node's height after
        #corresponding node in 'update' list
        for level in range(node_height):
            prevnode = update[level]
            newnode.next[level] = prevnode.next[level]
            prevnode.next[level] = newnode
            newnode.width[level] = prevnode.width[level] - steps
            prevnode.width[level] = steps + 1
            steps += steps_at_level[level]
        for level in range(node_height, self._max_levels):
            update[level].width[level] += 1
        self._size += 1
        self._max_levels = max(self._max_levels, node_height)


    def remove(self, data):
        '''Removes node with given data. Raises KeyError if
            data is not in list.'''
        update = [None]*self._max_levels
        node = self.head
        for level in reversed(range(self._max_levels)):
            while node.next[level].data < data:
                node = node.next[level]
            update[level] = node
        if data != update[0].next[0].data:
            raise KeyError('Not found')

        node = update[0].next[0]
        node_height = len(node.next)
        for level in range(node_height):
            prevnode = update[level]
            prevnode.width[level] += prevnode.next[level].width[level] - 1
            prevnode.next[level] = prevnode.next[level].next[level]
            
        for level in range(node_height, self._max_levels):
            update[level].width[level] -= 1
        while self._max_levels > 1 and self.head.next[level] == nil:
            self._max_levels -= 1
        del node
        self._size -= 1
        










        
if __name__ == '__main__':
    new = skiplist(0.5)
    for i in range(1, 6):
        new.insert(i)
    print new
    print new[0]
    new.remove(3)
    print new
