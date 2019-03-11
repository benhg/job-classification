print("Problem 5.14: Gravitational Pull of Galaxy, (a)")
from numpy import *
from pylab import *


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


z = 1
L = 10
G = 6.67*10**-11
m = 10000000000  # kg
SIGMA = (m/L**2)


def force_function(x_0, y_0, x_f,  y_f):
    return G*SIGMA*z*trapezoidal_2d(lambda x, y: 1/((x**2+y**2+z**2))**1.5, x_0, y_0, x_f,  y_f, .01)


print("FORCE WHERE Z=1:", force_function(-5, -5, 5, 5))

print("Problem 5.14: Gravitational Pull of Galaxy, (b)")

xs = linspace(0, 10, 100)
ys = []
z = 0.
for i in linspace(0, 10, 100):
    z = i + .01
    ys.append(force_function(-5, -5, 5, 5))

plot(xs, ys)
show()
