from sys import argv

# Fibonacci sequence
def fib(n):
    a = b = 1
    for i in range(n - 1):
        a, b = b, a + b
    print a

fib(int(argv[1]))
