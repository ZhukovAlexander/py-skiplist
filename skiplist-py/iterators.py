class LevelNodeIterator(object):
    def __init__(self, skip_list, level=0):
        self.s = skip_list
        self.l = level

    def __iter__(self):
        node = self.s.head.next[self.l]
        while node.next:
            yield node
            node = node.next[self.l]
        raise StopIteration
