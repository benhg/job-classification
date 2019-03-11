from numpy import *
from math import *


def trapezoid_integral(f, a, b, h):
    return h * (f(a)/2 + f(b)/2 + sum([f(a+(j*h)) for j in range(1, int((b-a)/h))]))


def f(x):
    return exp(-x**2)


def adaptive_trapezoidal(f, a, b, delta):
    h = .001
    n = (b-a)/h
    I_1 = trapezoid_integral(f, a, b, h)
    err = 1000
    while err > delta:
        h /= 2
        n *= 2
        next_int = I_1/2 + h*(sum([f(a+k*h) for k in range(1, int(n), 2)]))
        err = abs(next_int - I_1)/3
        if err < delta:
            return next_int, err
        else:
            I_1 = next_int


def adaptive_infinite_integral(f, a, b, delta):
    def g(z):
        return (1/((1-z)**2))*(f(-z/(1-z)+a))

    return adaptive_trapezoidal(g, a, b, delta)


def trapezoidal_2d(f, ax, ay, bx, by, h):
    nx = int((bx-ax) / h)
    ny = int((by-ay) / h)
    integral = 0

    for i in range(nx+1):
        for k in range(ny+1):
            l = f(ax+i*h, ay+k*h) * h**2
            if i == 0 or i == nx:
                l /= 2
            if k == 0 or k == ny:
                l /= 2
            integral += l
    return integral


def j(x, y):
    z = 1
    G = 1
    return G * z * (1)/pow((x**2 + y**2 + z**2), 1.5)


if __name__ == "__main__":
    print(trapezoidal_2d(j, -.5, -.5, .5, .5, .001))
