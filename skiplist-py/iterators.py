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


class AllNodesIterator(object):
    def __init__(self, skip_list, l_num):
        self.s = skip_list
        self.l_num = l_num

    def __iter__(self):
        return (node for level in reversed(range(self.l_num)) for node in LevelNodeIterator(self.s, level))
