# Find things in a string representing a number.

import operator
import itertools

# This can be done using a generator
num = ("73167176531330624919225119674426574742355349194934"
"96983520312774506326239578318016984801869478851843"
"85861560789112949495459501737958331952853208805511"
"12540698747158523863050715693290963295227443043557"
"66896648950445244523161731856403098711121722383113"
"62229893423380308135336276614282806444486645238749"
"30358907296290491560440772390713810515859307960866"
"70172427121883998797908792274921901699720888093776"
"65727333001053367881220235421809751254540594752243"
"52584907711670556013604839586446706324415722155397"
"53697817977846174064955149290862569321978468622482"
"83972241375657056057490261407972968652414535100474"
"82166370484403199890008895243450658541227588666881"
"16427171479924442928230863465674813919123162824586"
"17866458359124566529476545682848912883142607690042"
"24219022671055626321111109370544217506941658960408"
"07198403850962455444362981230987879927244284909188"
"84580156166097919133875499200524063689912560717606"
"05886116467109405077541002256983155200055935729725"
"71636269561882670428252483600823257530920752963450")

k = 13

# Generator expression method
print max(reduce(operator.mul, itertools.imap(int, num[i:i+k])) for i in
          xrange(len(num) - (k - 1)))

# Finding a sequence of numbers in the string.
seqs = [str(i * i) for i in xrange(20)]
exists_message = ('does not exist', 'exists')

for seq in seqs:
    exists = any(num[i:i+len(seq)] == seq for i in xrange(len(num) - len(seq) + 1))
    print "{0} {1}".format(seq, exists_message[exists])

# Rolling ~hash to search for seq.
def rolling_checks(n, seq):
    ceiling = 10 ** (len(seq) - 1)
    h = int(n[:len(seq)])
    yield h == int(seq)
    for i in xrange(len(n) - len(seq)):
        h = h % ceiling * 10 + int(n[i + len(seq)])
        yield h == int(seq)

for seq in seqs:
    exists = any(rolling_checks(num, seq))
    print "{0} {1}".format(seq, exists_message[exists])

uniques = dict.fromkeys(num).keys()
print uniques

count = dict()
for c in num:
    count[c] = count.get(c, 0) + 1
print count

reverse_count = dict(zip(count.itervalues(), count.iterkeys()))
for count in sorted(count.itervalues()):
    print "%s: %s" % (count, reverse_count[count])

references = dict()
for i, c in enumerate(num):
    references.setdefault(c, []).append(i)

for i in range(10):
    print i
    print references[str(i)]
    print

"""
# Generator method DOESN'T WORK! DIVISION BY ZERO!
def products(n, k):
    prod = reduce(lambda x, y: int(x) * int(y), n[:k])
    for i in xrange(len(num) - (k - 2)):
        prod = prod / int(n[i]) * int(n[i + k])
        yield prod

print max(products(num, k))
"""
