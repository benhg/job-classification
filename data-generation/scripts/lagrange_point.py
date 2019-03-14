from pylab import *
from math import *
from numpy import *


G = 6.674 * 10**-11
M = 5.974 * 10**24
m = 7.348 * 10**22
R = 3.844 * 10**8
omega = 2.662 * 10**-6


def lagrange_point_polynomial(r):
    return ((G * M) / r**2) - ((G * m) / (R - r)**2) - omega**2 * r


def dx(f, x):
    return (f(x + .01) - f(x)) / .01


def naive_Newton(f, dfdx, x, eps):
    while abs(f(x)) > eps:
        x = x - float(f(x)) / dfdx(f, x)
    return x


print(("The L1 Point for Earth Moon is located near r=%s" %
       naive_Newton(lagrange_point_polynomial, dx, 1000, 0.001)))
