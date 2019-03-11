from pylab import *
from numpy import zeros
from math import log, sqrt, sin, cos, pi
from random import random

Z = 79
little_e = 1.6e-19
E = 7.7e6*little_e
e_0 = 8.85e-12
SIGMA = 5.2e-11/100
N = 1000000


x = []
normx = []
normy = []
y = []

for i in range(N):
    z = random()
    x.append(i)
    y.append(z)
    theta = random() * 2 * pi
    normx.append(sqrt((-2 * SIGMA**2) * log(1-z)) * cos(theta))
    normy.append(sqrt((-2 * SIGMA**2) * log(1-z)) * sin(theta))


"""
plot(normy, y, "k.")
show()
plot(normy, normx, "k")
show()
"""

bcrit = (Z * little_e**2)/(2*pi*e_0*E)
print(bcrit)
backscatters = 0
for i in range(len(normx)):
    b = sqrt(normx[i]**2 + normy[i]**2)
    if b <= bcrit:
        backscatters += 1

print(backscatters)
