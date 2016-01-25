# Sort anagrams
from sys import argv

def sort_anagrams(anagrams):
    # step1: turn each anagram into a frozenset and map the anagram string to the frozenset.
    mapping = dict()
    for anagram in anagrams:
        count = dict()
        for c in anagram:
            count[c] = count.get(c, 0) + 1
        mapping.setdefault(frozenset(count.items()), []).append(anagram)
    # step2: return the strings using the frozenset map.
    return [anagram for key in mapping for anagram in mapping[key]]

print sort_anagrams(argv[1:])
