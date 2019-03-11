# PROBLEM 2
from math import *
from numpy import *
from pylab import *
import numpy as np

print("PROBLEM 2B")


def potential_function(theta):
    x, y, z = 1, 4, 7
    return ((1)/(4*pi))*((1)/(sqrt((3*cos(theta)-x)**2+(2*sin(theta)-y)**2)+(z)**2))


def field_function(theta):
    x, y, z = 1, 2, 5
    return ((1)/(4*pi))*((sqrt(x**2+y**2+z**2))/((3*cos(theta)-x)**2 + (2 * sin(theta) - y)**2 + z**2))


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


integrated_potential = simpson_integrate(potential_function, 0, 2*pi, .1)

integrated_field = simpson_integrate(field_function, 0, 2*pi, .1)


def simps_err(f, a, b, h):
    return -1*(1/90)*(h)**5*(f((b-a)/2))


int_error = simps_err(potential_function, 0, 2*pi, .1)
field_err = simps_err(field_function, 0, 2*pi, .1)
print("Integral Estimate for Potential: ",
      integrated_potential, "Estimated Error:", int_error)

print("Integral Estimate for Field: ",
      integrated_field, "Estimated Error:", field_err)


print("PROBLEM 2C")


def trapezoid_integral(f, a, b, h):
    return h * (f(a)/2 + f(b)/2 + sum([f(a+(j*h)) for j in range(1, int((b-a)/h))]))


def adaptive_trapezoidal(f, a, b, delta):
    h = .001
    n = (b-a)/h
    I_1 = trapezoid_integral(f, a, b, h)
    err = 1000
    while err > delta:
        h /= 2
        n *= 2
        next_int = I_1/2 + h*(sum([f(a+k*h) for k in range(1, int(n), 2)]))
        err = abs(next_int - I_1)/3
        if err < delta:
            return next_int, err
        else:
            I_1 = next_int


trap_field, t_err = adaptive_trapezoidal(field_function, 0, 2*pi, .001)
print("Adaptive trapezoidal for field:", trap_field, "Error:", t_err)


print("Problem 2D")


def potential_function(theta, x, y, z):
    return ((1)/(4*pi))*((1)/(sqrt((3*cos(theta)-x)**2+(2*sin(theta)-y)**2)+(z)**2))


def simpson_integrate(f, a, b, h, x, y, z):

    n = int(abs(b - a)/h)
    if n % 2 != 0:
        n -= 1

    sum1 = 0
    s3 = 0
    for i in range(1, n, 2):
        s3 += f(a + (i*h), x, y, z)
    s3 *= 4
    sum1 += s3
    sum2 = 0
    s4 = 0
    for i in range(2, n-1, 2):
        s4 += f(a + i*h, x, y, z)
    s4 *= 2
    sum2 = s4
    approx = h/(3.0)*(f(a, x, y, z) + f(b, x, y, z) + sum1 + sum2)
    return approx


density_data = [[simpson_integrate(potential_function, 0, 2*pi, .1, .01*i, .01*j, 0)
                 for j in range(-100, 100)] for i in range(-100, 100)]

imshow(density_data)
show()
