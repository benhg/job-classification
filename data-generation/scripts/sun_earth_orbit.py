from pylab import *
from numpy import *
import numpy as np

GMs = 4 * pi**2


def f1(x, y, vx, vy, t):
    return vx


def f2(x, y, vx, vy, t):
    return vy


def f3(x, y, vx, vy, t):
    return -(GMs * x) / ((x**2 + y**2)**(3 / 2))


def f4(x, y, vx, vy, t):
    return -(GMs * y) / ((x**2 + y**2)**(3 / 2))


def solar_system_rk4(r0, v0, f1, f2, f3, f4, tmax):

    xpts = []
    ypts = []
    vxpts = []
    vypts = []
    h = .01
    x = r0
    y = 0
    vx = 0
    vy = v0
    tpoints = arange(0, tmax, h)
    for t in tpoints:
        k1 = h * f1(x, y, vx, vy, t)
        l1 = h * f2(x, y, vx, vy, t)
        m1 = h * f3(x, y, vx, vy, t)
        n1 = h * f4(x, y, vx, vy, t)
        k2 = h * f1(x + k1 / 2, y + l1 / 2, vx +
                    m1 / 2, vy + n1 / 2, t + h / 2)
        l2 = h * f2(x + k1 / 2, y + l1 / 2, vx +
                    m1 / 2, vy + n1 / 2, t + h / 2)
        m2 = h * f3(x + k1 / 2, y + l1 / 2, vx +
                    m1 / 2, vy + n1 / 2, t + h / 2)
        n2 = h * f4(x + k1 / 2, y + l1 / 2, vx +
                    m1 / 2, vy + n1 / 2, t + h / 2)
        k3 = h * f1(x + k2 / 2, y + l2 / 2, vx +
                    m2 / 2, vy + n2 / 2, t + h / 2)
        l3 = h * f2(x + k2 / 2, y + l2 / 2, vx +
                    m2 / 2, vy + n2 / 2, t + h / 2)
        m3 = h * f3(x + k2 / 2, y + l2 / 2, vx +
                    m2 / 2, vy + n2 / 2, t + h / 2)
        n3 = h * f4(x + k2 / 2, y + l2 / 2, vx +
                    m2 / 2, vy + n2 / 2, t + h / 2)
        k4 = h * f1(x + k3, y + l3, vx + m3, vy + n3, t + h)
        l4 = h * f2(x + k3, y + l3, vx + m3, vy + n3, t + h)
        m4 = h * f3(x + k3, y + l3, vx + m3, vy + n3, t + h)
        n4 = h * f4(x + k3, y + l3, vx + m3, vy + n3, t + h)
        x = x + 1 / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        y = y + 1 / 6 * (l1 + 2 * l2 + 2 * l3 + l4)
        vx = vx + 1 / 6 * (m1 + 2 * m2 + 2 * m3 + m4)
        vy = vy + 1 / 6 * (n1 + 2 * n2 + 2 * n3 + n4)
        xpts.append(x)
        ypts.append(y)
        vxpts.append(vx)
        vypts.append(vy)

    return xpts, ypts, vxpts, vypts, tpoints


xpts, ypts, vxpts, vypts, tpts = solar_system_rk4(
    1, 2 * pi, f1, f2, f3, f4, 100)
plot(xpts, ypts, )
show()
