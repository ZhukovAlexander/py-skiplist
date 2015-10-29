# __author__ = 'azhukov'
# import cProfile
# import random
#
# from py_skiplist.skiplist import Skiplist
# from py_skiplist.iterators import geometric
from bintrees import RBTree
#
# DATA_SET = [random.randint(1, 10**3) for i in range(100000)]
# READ_INPUT = [random.randint(1, 10**3) for j in range(1)]
#
# def run_skiplist_test():
#     sl = Skiplist()
#     for c in DATA_SET:
#         sl._insert(c, c)
#     # print sum(len(node.nxt) for node in sl._level(level=0))
#     # print [len(node.nxt) for node in sl._level(level=0)]
#     # g = geometric(0.5)
#     # print [next(g) for _ in range(200)]
#     return sl
#
# sl = run_skiplist_test()
# # print sum(len(node.nxt) for node in sl._level(level=0))
# print [len(node.nxt) for node in sl._level(level=0)]
# # g = geometric(0.5)
# print [next(sl.distribution) +1  for _ in range(200)]
#
#
# def sl_read():
#     for j in READ_INPUT:
#         sl.get(i)
#     # print sl.n, sl.nc, ncals
#     # print sum(len(node.nxt) for node in sl._level())
#
# def run_rbtree_test():
#     tree = RBTree()
#     for i in DATA_SET:
#         tree[str(i)] = i
#     return tree
#
# tree = run_rbtree_test()
#
# def tree_read():
#     for k in READ_INPUT:
#         tree.get(k)
#
# # cProfile.run('sl._insert(5000, 30)')
# cProfile.run('run_skiplist_test()')
# cProfile.run('run_rbtree_test()')
# # cProfile.run('sl_read()')
# # cProfile.run('tree_read()')
#
# from pycallgraph import PyCallGraph
# from pycallgraph.output import GraphvizOutput
#
# # with PyCallGraph(output=GraphvizOutput()):
# #     run_skiplist_test()