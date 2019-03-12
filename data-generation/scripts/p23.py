from math import sqrt

def d(n):
    sum = 1
    t = sqrt(n)
    # only proper divisors; start from 2.
    for i in range(2, int(t)+1):
        if n % i == 0:
            sum += i + n / i
    # don't count the square root twice!
    if t == int(t):
        sum -= t
    return sum

limit = 20162
sum = 0
# it's a set, after all. sets are faster than lists for our needs.
abn = set()
for n in range(1, limit):
    if d(n) > n:
        abn.add(n)
    # if the difference of the number we're examining and every number in the set
    # is in the set, then the number is the sum of two abundant numbers.
    # otherwise, we must add it to our sum in question.
    if not any( (n-a in abn) for a in abn ):
        sum += n
print(sum)