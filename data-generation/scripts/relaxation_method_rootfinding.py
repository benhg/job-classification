from numpy.linalg import *
from math import *


def f(x):
    return sqrt(1 - log(x))


err = 10**-5

X = .5
y = 0
z = 0
while abs(f(X) - X) > err:
    y = f(X)
    X = y
    z += 1
    if z > 1000:
        print("Did not converge.")
        exit(1)


print((X, y))
