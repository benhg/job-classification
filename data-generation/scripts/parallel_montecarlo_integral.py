from math import *
import random
from pylab import *
from numpy import *
import multiprocessing


def f(x):
    return sin(1 / (x * (2 - x)))**2


def worker(dist, height=1, a=0):
    x, y = (random.random() * dist), random.random() * height
    if y < f(x):
        return 1
    return 0


def mc_int(f, a, b, n, height):
    dist = b - a
    pool = multiprocessing.Pool()
    work = pool.map(worker, [dist for i in range(n)])
    return dist ** height * (sum(work) / n)


#plot(linspace(0, 2, 1000), [f(x) for x in linspace(0, 2, 1000)])
# show()
print((mc_int(f, 0, 2, 10**7, 1)))
