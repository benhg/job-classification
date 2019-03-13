from math import*
from pylab import*
from numpy import*
import numpy as np
import time


w=0.905
a=1

def rho(x,y):
    if x==50 and 50<y<150:
        return 1
    elif x==150 and 50<y<150:
        return 1
    elif y==50 and 50<x<150:
        return 1
    elif y==150 and 50<x<150:
        return 1
    else:
        return 0

N = 200


phi = zeros([N,N],float)



error = 100
tolerance = 10**-3

timeBefore = time.time()

while error>tolerance:
    biggestDiff = 0
    for i in range(0,N):
        for j in range(0,N):
            if i==0 or i==N-1 or j==0 or j==N-1:
                pass
            else:
                newValue = ((1+w)/4)*(phi[i-1][j]+phi[i+1][j]+phi[i][j-1]+phi[i][j+1])-w*phi[i][j]+a**2/4*rho(j,i)
                diff = abs(phi[i,j]-newValue)
                if diff > biggestDiff:
                    biggestDiff = diff
                phi[i,j] = newValue
    error = biggestDiff
    
timeAfter = time.time()
total=timeAfter - timeBefore
print(('It took',total,'seconds'))

print(("V at (0,0) is {}".format(phi[100][100])))
print(("V at (0,.25) is {}".format(phi[125][100])))


def dVdx(x,y):
    h = 1
    return (phi[x+h][y] - phi[x][y])/h

def dVdy(x,y):
    h = 1
    return (phi[x][y+h] - phi[x][y])/h

def E(x,y):
    return (-(dVdx(x,y)), -(dVdy(x,y)))


print(("E at (0,0) is {}".format(E(100,100))))
print(("E at (0,.25) is {}".format(E(125, 100))))

imshow(phi)
show()


