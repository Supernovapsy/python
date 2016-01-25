from sys import argv

# Fibonacci sequence
def fib(n):
    a = b = 1
    for i in range(n):
        print a
        a, b = b, a + b

fib(int(argv[1]))
