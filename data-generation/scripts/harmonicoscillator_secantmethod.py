from numpy import array, arange
from pylab import *
from math import *
from scipy.integrate import simps

# Constants
m = 9.1094e-31     # Mass of electron
hbar = 1.0546e-34  # Planck's constant over 2*pi
e = 1.6022e-19     # Electron charge
L = 5.2918e-11     # Bohr radius
N = 1000
h = L / N
V0 = 50 * e
a = 10**-11

# Potential function


def V(x):
    return (V0 * x**2) / a**2


def f(r, x, E):
    psi = r[0]
    phi = r[1]
    fpsi = phi
    fphi = (2 * m / hbar**2) * (V(x) - E) * psi
    return array([fpsi, fphi], float)

# Calculate the wavefunction for a particular energy


def solve(E):
    psi = 0.0
    phi = 1.0
    r = array([psi, phi], float)
    y = []
    for x in arange(-5 * a, 5 * a, h):
        k1 = h * f(r, x, E)
        k2 = h * f(r + 0.5 * k1, x + 0.5 * h, E)
        k3 = h * f(r + 0.5 * k2, x + 0.5 * h, E)
        k4 = h * f(r + k3, x + h, E)
        r += (k1 + 2 * k2 + 2 * k3 + k4) / 6
        y.append(abs(r[0])**2)

    return r[0], y


# Main program to find the energy using the secant method
E1 = 0.0
E2 = e
psi2, y1 = solve(E1)

target = e / 1000
while abs(E1 - E2) > target:
    psi1, psi2 = psi2, solve(E2)[0]
    y1 = solve(E2)[1]
    E1, E2 = E2, E2 - psi2 * (E2 - E1) / (psi2 - psi1)

int1 = simps([abs(i)**2 for i in y1], dx=h)
print(("E =", E2 / e, "eV"))


E1 = 300 * e
E2 = 500 * e
psi2, y5 = solve(E1)

target = e / 1000
while abs(E1 - E2) > target:
    psi1, psi2 = psi2, solve(E2)[0]
    y2 = solve(E2)[1]
    E1, E2 = E2, E2 - psi2 * (E2 - E1) / (psi2 - psi1)

int2 = simps([abs(i)**2 for i in y2], dx=h)
print(("E =", E2 / e, "eV"))

E1 = 900 * e
E2 = 1200 * e
psi2, y7 = solve(E1)

target = e / 1000
while abs(E1 - E2) > target:
    psi1, psi2 = psi2, solve(E2)[0]
    y3 = solve(E2)[1]
    E1, E2 = E2, E2 - psi2 * (E2 - E1) / (psi2 - psi1)

int3 = simps([abs(i)**2 for i in y3], dx=h)
print(("E =", E2 / e, "eV"))


plot(arange(-5 * a, 5 * a, h)[:-100], [abs(i)**2 / int1 for i in y1][:-100])
plot(arange(-5 * a, 5 * a, h)[:-100], [abs(i)**2 / int2 for i in y2][:-100])
plot(arange(-5 * a, 5 * a, h)[:-100], [abs(i)**2 / int3 for i in y3][:-100])
show()
