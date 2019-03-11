from math import *
from pylab import *
import numpy as np

M = 100
xsi = .01
Phi = np.zeros([M, M], float)
PhiP = np.zeros([M, M], float)


def dfdx(i, j):
    if i != M-1:
        return Phi[i+1, j]-Phi[i, j]
    else:
        return Phi[i, j]-Phi[i-1, j]


def dfdy(i, j):
    if j != M-1:
        return Phi[i, j+1]-Phi[i, j]
    else:
        return Phi[i, j]-Phi[i, j-1]


error = 100
delta = 10**(-1)
R1 = 75
R2 = 25


def eta(i, j):
    if(i == 50):
        return 0
    return atan((j-R2)/(i-50))-atan((j-R1)/(i-50))


while(error > delta):
    for i in range(0, M):
        for j in range(0, M):
            if(i == 0 or j == 0 or i == M-1 or j == M-1):
                PhiP[i][j] = Phi[i][j]
            else:
                PhiP[i][j] = (Phi[i+1][j]+Phi[i-1][j]+Phi[i][j+1] +
                              Phi[i][j-1])/4+(-xsi)*sin(2*(Phi[i][j]+eta(i, j)))/4
    error = np.max(np.abs(Phi-PhiP))
    Phi, PhiP = PhiP, Phi

imshow(Phi)
show()


L = np.zeros([M, M], float)
for i in range(0, M):
    for j in range(0, M):
        L[i][j] = (dfdx(i, j)**2+dfdy(i, j)**2+xsi *
                   (cos(2*(Phi[i][j]+eta(i, j))))/2)


imshow(L)
show()
