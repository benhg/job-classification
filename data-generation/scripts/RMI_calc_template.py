# HOMEWORK 2 Reading from a data file. Fill in the area for the integrand.
from numpy import loadtxt
from pylab import plot, show, xlim, legend, xlabel, ylabel, title
from math import *

data = loadtxt('data1.txt')  # loads the data file
T_plot = data[0]  # plot of temperatures
E_1 = data[1]  # plot of first energy
E_2 = data[3]  # plot of second energy
E_3 = data[5]  # plot of third energy

count = len(T_plot)  # number of temperature points

deltaT = 0.1

# Fill in this space with the calculation of RMI for each temperature:
### CODE ##


def simpson_integrate(f, a, b, h):

    n = int(abs(b - a)/h)
    if n % 2 != 0:
        n -= 1

    sum1 = 0
    s3 = 0
    for i in range(1, n, 2):
        s3 += f(a + (i*h))
    s3 *= 4
    sum1 += s3
    sum2 = 0
    s4 = 0
    for i in range(2, n-1, 2):
        s4 += f(a + i*h)
    s4 *= 2
    sum2 = s4
    approx = h/(3.0)*(f(a) + f(b) + sum1 + sum2)
    return approx


def rmi(t):
    def inner_func(t):
        return (2*E_1[int(t*10)] - E_2[int(t*10)] - 2*E_3[int(t*10)])/t**2

    integr = simpson_integrate(inner_func, t, 99, deltaT)
    return integr


rmis = []
for i in range(0, 1000, 10):
    rmis.append(rmi(.1*i))

print(rmis)


print("Now Estimating Error. Simpson error <= -(1/90)((Tmax-T)/2)**5*f^(4)((Tmax-T)/2)")


def inner_func(t):
    return (2*E_1[int(t*10)] - E_2[int(t*10)] - 2*E_3[int(t*10)])/t**2


def simps_err(f, a, b, h):
    return -1*(1/90)*(deltaT)**5*(f((b-a)/2))


print((simps_err(inner_func, 0, 100, .1)))

### CODE ###
plot([.1*i for i in range(0, 1000, 10)], rmis, label='RMIs')
plot(T_plot, E_1, label='Energy 1')
plot(T_plot, E_2, label='Energy 2')
plot(T_plot, E_3, label='Energy 3')
xlabel('Temperature (K)')
ylabel('Energy (J)')
title('Energy')
xlim(0, 100)
legend()
show()
