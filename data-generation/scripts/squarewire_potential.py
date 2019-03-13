from math import *

def trapezoidal_2d(f, ax, ay, bx, by, h):
    nx = int((bx-ax) / h)
    ny = int((by-ay) / h)
    integral = 0

    for i in range(nx+1):
        for k in range(ny+1):
            l = f(ax+i*h, ay+k*h) * h**2
            if i == 0 or i == nx:
                l /= 2
            if k == 0 or k == ny:
                l /= 2
            integral += l
    return integral


def adaptive_trapezoidal_2d(f, ax, ay, bx, by, delta):
    h = 10**-1
    ny = (by-ay)/h
    nx = (bx-ax)/h
    I_1 = trapezoidal_2d(f, ax, ay, bx, by, h)
    err = 1000
    while err > delta:
        h /= 2
        nx *= 2
        ny *= 2
        next_int = I_1/2 + h*(sum([f(ax+k*h, ay) for k in range(1, int(nx), 2)]))+ h*(sum([f(ax, ay+k*h) for k in range(1, int(ny), 2)]))
        err = abs(next_int - I_1)/3
        if err < delta:
            
            return next_int, err
        else:
            I_1 = next_int



def rho(x, y):
    if x == 1/2 and -1/2 <= y <= 1/2:
        return 1
    elif x == -1/2 and -1/2 <= y <= 1/2:
        return 1
    elif y == 1/2 and -1/2 <= x <= 1/2:
        return 1
    elif y == -1/2 and -1/2 <= x <= 1/2:
        return 1
    else:
        return 0


def function_to_integrate_00(x,y):
    a, b = 0,0
    r = [a,b]
    rprime = [x,y]
    dist = sqrt(sum([(a-x)**2, (b-y)**2]))
    try:
        return rho(x, y)/(dist)
    except Exception as e:
        pass


print(("The total field at point(x, y) = (0, 0) is {}".format(
    adaptive_trapezoidal_2d(function_to_integrate_00, -1/2, -1/2, -1/2, 1/2, 10**-3)[0]
    + adaptive_trapezoidal_2d(function_to_integrate_00, -1/2, -1/2, 1/2, -1/2, 10**-3)[0]
    + adaptive_trapezoidal_2d(function_to_integrate_00, 1/2, -1/2, 1/2, 1/2, 10**-3)[0]
    + adaptive_trapezoidal_2d(function_to_integrate_00, -1/2, 1/2, 1/2, 1/2, 10**-3)[0])))

def function_to_integrate_140(x,y):
    a, b = 1/4,0
    r = [a,b]
    rprime = [x,y]
    dist = sqrt(sum([(a-x)**2, (b-y)**2]))
    try:
        return rho(x, y)/(dist)
    except Exception as e:
        pass


print(("The total field at point(x, y) = (1/4, 0) is {}".format(
    adaptive_trapezoidal_2d(function_to_integrate_140, -1/2, -1/2, -1/2, 1/2, 10**-3)[0]
    + adaptive_trapezoidal_2d(function_to_integrate_140, -1/2, -1/2, 1/2, -1/2, 10**-3)[0]
    + adaptive_trapezoidal_2d(function_to_integrate_140, 1/2, -1/2, 1/2, 1/2, 10**-3)[0]
    + adaptive_trapezoidal_2d(function_to_integrate_140, -1/2, 1/2, 1/2, 1/2, 10**-3)[0])))


from numpy import zeros, linspace
import multiprocessing as mp

phi = []
SIZE = 1


for i, loc1 in enumerate(linspace(-SIZE, SIZE, 100)):
    def worker(tup):
        
        j = tup[0] 
        loc2 = tup[1]
        def function_to_integrate_140(x,y):
            a, b = loc1,loc2
            r = [a,b]
            rprime = [x,y]
            dist = sqrt(sum([(a-x)**2, (b-y)**2]))
            try:
                return rho(x, y)/(dist)
            except Exception as e:
                pass
            
        def total_integral(x, y):
            inte = adaptive_trapezoidal_2d(function_to_integrate_140, -1/2, -1/2, -1/2, 1/2, 10**-3)[0] + adaptive_trapezoidal_2d(function_to_integrate_140, -1/2, -1/2, 1/2, -1/2, 10**-3)[0]+ adaptive_trapezoidal_2d(function_to_integrate_140, 1/2, -1/2, 1/2, 1/2, 10**-3)[0]+ adaptive_trapezoidal_2d(function_to_integrate_140, -1/2, 1/2, 1/2, 1/2, 10**-3)[0]
            if y == 0:
                print(("{}.{} percent complete".format(x, y)))
            return  inte
        
        return total_integral(i, j)
        
    pool = mp.Pool()
    phis = pool.map(worker, enumerate(linspace(-SIZE, SIZE, 100)))
    phi.append(phis)
    pool.close()



from pylab import *
imshow(phi)
show()


## AFTER THE PHI EXISTS, THIS PART SHOULD JUST WORK. TRANSLATE X,Y TO POINTS IN PHI

def dVdx(x,y):
    h = 1
    return (phi[x+h][y] - phi[x][y])/h

def dVdy(x,y):
    h = 1
    return (phi[x][y+h] - phi[x][y])/h

def E(x,y):
    return (-(dVdx(x,y)), -(dVdy(x,y)))


print((E(50, 50), E(62, 50)))
