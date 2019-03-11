import sys
from pylab import *
import time

n = 100

a = 1664525
c = 1013904223
m = 4294967296

X = time.time()

all_xs = []

for i in range(n):
    X = (((a * X) + c) % m) / m
    all_xs.append(X)

plot(range(n), all_xs, ".k")
show()
