from itertools import dropwhile, count, cycle
import random


def geometric(p):
    return (next(dropwhile(lambda _: random.randint(1, int(1. / p)) == 1, count())) for _ in cycle([1]))


def uniform(n):
    """
    Simple deterministic distribution for testing internal of the skiplist
    """
    return (n for _ in cycle([1]))
