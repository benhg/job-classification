from numpy.linalg import solve
from numpy import *

A = array([[1, 2], [5, 6]], float)
V = array([9, 10], float)

x = solve(A, V)
print(x)
