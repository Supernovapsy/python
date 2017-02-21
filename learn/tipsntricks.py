#!/usr/bin/python

# works if a is a sequence.
group_adj = lambda a, k: zip(*([iter(a)] * k))

def zip_inv():
    a = tuple('asdfiwqe')
    b = tuple(xrange(8))
    c = [a, b]
    if zip(*zip(*c)) == c:
        print "zip is an involution on lists of equal-sized tuples!"

zip_inv()

print group_adj('abcdefghi', 3)

"""
Other tips not yet shown:
exec
execfile
eval
globals
locals
changing function definition at runtime.
Interview questions.

"""
