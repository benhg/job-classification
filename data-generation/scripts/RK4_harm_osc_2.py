# RK4 on a double differential eqn.
# Cleaner version of RK4_harmonic_oscillator.py

from numpy import arange
from pylab import *
l = 9.8
g = l
delta = 0


def f1(theta, omega, t):
    return omega


def f2(theta, omega, t):
    return -(g/l)*sin(theta)


theta = .1
omega = 0

thetapoints = []
omegapoints = []
tpoints = arange(0, 10, .1)
h = .1
for t in tpoints:
    thetapoints.append(theta)
    omegapoints.append(omega)
    k1 = h * f1(theta, omega, t)
    l1 = h * f2(theta, omega, t)
    k2 = h*f1(theta+k1/2, omega+l1/2, t+h/2)
    l2 = h*f2(theta+k1/2, omega+l1/2, t+h/2)
    k3 = h*f1(theta+k2/2, omega+l2/2, t+h/2)
    l3 = h*f2(theta+k2/2, omega+l2/2, t+h/2)
    k4 = h*f1(theta+k3, omega+l3, t+h/2)
    l4 = h*f2(theta+k3, omega+l3, t+h/2)
    theta = theta + 1/6 * (k1 + 2*k2 + 2*k3 + 2*k4)
    omega = omega + 1/6 * (l1 + 2*l2 + 2*l3 + l4)


plot(thetapoints, omegapoints)
axes().set_aspect("equal")
show()
