# square of sums - sum of squares.
import operator

cum_sum = lambda n: n * (n + 1) / 2
cum_sq = lambda n: reduce(operator.add, map(lambda a: a ** 2, xrange(1, n + 1)))

n = 3

print cum_sum(n)**2 - cum_sq(n)

"""
# Version 2

import operator
import itertools # Improvement using iterator maps.

cum_sum = lambda n: n * (n + 1) / 2
cum_sq = lambda n: reduce(operator.add, itertools.imap(lambda a: a ** 2, xrange(1, n + 1)))

n = 100

print cum_sum(n)**2 - cum_sq(n)
"""
