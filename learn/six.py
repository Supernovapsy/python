def is_prime(x):
    if x < 2:
        raise Exception("The number has to be >= 2")

    for i in range(2, x):
        if x % i == 0:
            return False
    return True

# Time complexity is O((1/2) * (n^2 - n) + 1)
primes = [i for i in range(2, 101) if is_prime(i)]
print primes

# x^5 + x^4 * sin(x) = O(x^5), but is not omega(x^5)

primes2 = filter(is_prime, range(2, 101))
print primes2

print abs(-4)