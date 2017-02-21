#!/usr/bin/python
from sys import argv

def unique_chars(string):
    return len(dict.fromkeys(string).keys()) == len(string)

print unique_chars(argv[1])
