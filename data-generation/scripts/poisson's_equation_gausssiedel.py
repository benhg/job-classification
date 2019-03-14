

from math import*
from pylab import*
from numpy import*
import numpy as np
import time

w = 0.905
a = 1


def rho(x, y):
    if 60 < x < 80 and 20 < y < 40:
        return 1
    elif 60 < y < 80 and 20 < x < 40:
        return -1
    else:
        return 0


N = 100


phi = zeros([N, N], float)


error = 100
tolerance = 10**-6

timeBefore = time.time()

while error > tolerance:
    biggestDiff = 0
    for i in range(0, N):
        for j in range(0, N):
            if i == 0 or i == N - 1 or j == 0 or j == N - 1:
                pass
            else:
                newValue = ((1 + w) / 4) * (phi[i - 1][j] + phi[i + 1][j] + phi[i]
                                            [j - 1] + phi[i][j + 1]) - w * phi[i][j] + a**2 / 4 * rho(j, i)
                diff = abs(phi[i, j] - newValue)
                if diff > biggestDiff:
                    biggestDiff = diff
                phi[i, j] = newValue
    error = biggestDiff

timeAfter = time.time()
total = timeAfter - timeBefore
print(('It took', total, 'seconds'))
imshow(phi)
show()
