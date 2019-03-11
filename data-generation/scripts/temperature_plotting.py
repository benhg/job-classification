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

print("PROBLEM 3")


def E3(T):
    return E_3[T]


def derivative(f, x, dX=1):
    return (f(x+dX) - f(x))/(x+dX-x)


things = []
for i in range(count-1):
    things.append(derivative(E3, i))
things.append(derivative(E3, 996))


plot(T_plot, things, label="C(T)")
cmax = max(things)
print("C_MAX = ", cmax, "T = ", T_plot[things.index(cmax)])

plot(T_plot, E_3, label="E_3(T)")
title("E_3 and C vs T")
legend()
show()
