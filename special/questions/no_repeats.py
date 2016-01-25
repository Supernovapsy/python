# Given a string of characters, reorder them so that no character repeats
# consecutively in the string.

from sys import argv
import math
from collections import deque

def no_repeatify(s):
    count = dict()
    for c in s:
        count[c] = count.get(c, 0) + 1
    count = sorted(count.iteritems(), key=lambda x: x[1], reverse=True)
    if count[0][1] > math.ceil(len(s) / 2.0):
        return None

    chars = deque()
    for c, co in count:
        for i in xrange(co):
            chars.append(c)

    ret = range(len(s))
    for i in xrange(0, len(s), 2):
        ret[i] = chars.popleft()
    for i in xrange(1, len(s), 2):
        ret[i] = chars.popleft()

    return "".join(ret)

print no_repeatify(argv[1])
