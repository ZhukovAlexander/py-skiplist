from itertools import dropwhile, count, repeat
import random


def geometric(p):
    return (next(dropwhile(lambda _: random.randint(1, int(1. / p)) == 1, count())) for _ in repeat(1))


# Simple deterministic distribution for testing internals of the skiplist. 
uniform = repeat
