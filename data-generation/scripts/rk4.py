from numpy import *
from pylab import *


def f(x, t):
    return -x**3 + sin(t)


def rk_solve(f, a, b, h, x_0=0):
    N = abs((b-a)/h)
    x = x_0
    xpoints = []
    tpoints = arange(a, b, h)
    for t in tpoints:
        xpoints.append(x)
        k_1 = h*f(x, t)
        k_2 = h*f(x+.5*k_1, t+h/2)
        k_3 = h*f(x+.5*k_2, t+h/2)
        k_4 = h*f(x+.5*k_3, t+h)
        x = x + (1/6)*(k_1 + 2*k_2 + 2*k_3 + k_4)
    return xpoints, tpoints


def euler_solve(f, a, b, h, x_0=0):
    N = abs((b-a)/h)
    x = x_0
    xpoints = []
    tpoints = arange(a, b, h)
    for t in tpoints:
        xpoints.append(x)
        x = x + h * f(x, t)
    return xpoints, tpoints


a = 0
b = 10
h = 1
x_0 = 0
x, t = rk_solve(f, a, b, .01, x_0)
x2, t2 = euler_solve(f, a, b, .5, x_0)
plot(t, x, label="RK4")
plot(t2, x2, label="Euler")
legend()
show()
