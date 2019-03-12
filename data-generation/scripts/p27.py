from math import sqrt

def prime_sieve(n):
    sieve = [True] * (n/2)
    for i in xrange(3,int(sqrt(n))+1,2):
        if sieve[i/2]:
            sieve[i*i/2::i] = [False] * ((n-i*i-1)/(2*i)+1)
    return [2] + [2*i+1 for i in xrange(1,n/2) if sieve[i]]

def is_prime(n):
    if n <= 1: return False
    if n <= 3: return True
    if n%2==0 or n%3 == 0: return False
    r = int(sqrt(n))
    f = 5
    while f <= r:
        if n%f == 0 or n%(f+2) == 0: return False
        f+= 6
    return True

L = 1000
nmax = 0
for b in prime_sieve(L):
    for a in range(-b, b, 2):
        n = 1
        while is_prime(n*n + a*n + b): n += 1
        if n>nmax: nmax, p = n, a*b

print "Project Euler 27 Solution = ", p, "Sequence length =", nmax