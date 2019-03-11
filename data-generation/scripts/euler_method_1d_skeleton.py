from numpy import *
from pylab import *


def f(x, t):
    return -x**3 + sin(t)


def euler_solve(f, a, b, N, x_0=0):
    h = abs((b-a)/N)
    x = x_0
    xpoints = []
    tpoints = arange(a, b, h)
    for t in tpoints:
        xpoints.append(x)
        x = x + h * f(x, t)
    return xpoints, tpoints


a = 0
b = 10
N = 10000
x_0 = 0
x, t = euler_solve(f, a, b, N, x_0)
plot(t, x)
show()
