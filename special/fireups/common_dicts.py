def common_dicts(a, b):
    """Return common dicts in two lists."""
    s1 = {frozenset(d.iteritems()) for d in a}
    s2 = {frozenset(d.iteritems()) for d in b}
    # Each of s1 and s2 will be a set of frozensets of 2-tuples.
    # As a result, each frozenset inside s1 and s2 can be directly converted
    # into a dict.
    return [dict(s) for s in s1.intersection(s2)]

list1 = [{'a': 1, 'b': 2}, {'c': 3, 'd': 4}, {'e': 5, 'f': 6}]
list2 = [{'e': 5, 'f': 6}, {'g': 7, 'h': 8}, {'i': 9, 'j': 10}]
print common_dicts(list1, list2)

