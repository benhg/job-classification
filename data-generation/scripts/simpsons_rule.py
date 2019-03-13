from math import *


def simpson(f, a, b, h):

    n = int(abs(b - a)/h)
    if n % 2 != 0:
        n -= 1

    sum1 = 0
    s3 = 0
    for i in range(1, n, 2):
        s3 += f(a + (i*h))
    s3 *= 4
    sum1 += s3
    sum2 = 0
    s4 = 0
    for i in range(2, n-1, 2):
        s4 += f(a + i*h)
    s4 *= 2
    sum2 = s4
    approx = h/(3.0)*(f(a) + f(b) + sum1 + sum2)
    return approx


def function(x):
    return e**(-x**2)


def simpsArden(func, a, b, h):
    n = int(abs(b - a) / h)
    n -= 1 if n % 2 == 1 else 0
    return (h / 3)*(func(a) + func(b) +
                    4 * sum([func(a + k * h) for k in range(1, n, 2)]) +
                    2 * sum([func(a + k * h) for k in range(2, n - 1, 2)]))


print((simpson(function, 1, 2, .00001), simpsArden(function, 1, 2, .00001)))
