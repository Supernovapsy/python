import pickle
from sys import argv
from sys import stdout

list = pickle.Unpickler(open(argv[1])).load()

for l in list:
    for element in l:
        stdout.write(element[0] * element[1])
    print
