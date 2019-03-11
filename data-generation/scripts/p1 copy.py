print("Problem 1. Magnetic Field Integral")

from math import *
from pylab import *
from numpy import *


def numerator_of_integrated_function(x, y, z):
    """This function takes x,y,and z, treats them as constants (temporarilly), and returns a function of theta, which will return a vector. That vector will be the numerator for the function which needs to be integrated"""
    # [-3*sin(theta), 3*cos(theta), 0

    def f(theta):
        return cross([-3*sin(theta), 3*cos(theta), 0], [x-3*cos(theta), y-3*sin(theta), z])

    return f


def denominator_of_integrand(x, y, z):
    """This does the same thing that the function above does, but it does it for the denominator. This will return a scalar"""
    def g(theta):
        return ((x-3*cos(theta))**2 + (y-2*sin(theta))**2 + (z)**2)**(3/2)

    return g


def simpson_integrate(f, a, b, h):
    """Simpson's method integral function"""
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


def integrated_field(x, y, z, I):
    """Put together all of the things and make this function nicely return the field at a given point."""
    f = numerator_of_integrated_function(x, y, z)
    g = denominator_of_integrand(x, y, z)

    def integrable_func(theta):
        return f(theta)/g(theta)

    field = simpson_integrate(integrable_func, 0, 2*pi, .1)
    return I*field


print("Magnetic field at (x,y,z)=(1,4,7): ", integrated_field(1, 4, 7, 1))


print("Now, we will re-use the old code, to calculate at a different point using the adaptive trapezoidal method")


def adaptive_integrated_field(x, y, z, I, err):
    f = numerator_of_integrated_function(x, y, z)
    g = denominator_of_integrand(x, y, z)

    def integrable_func(theta):
        return f(theta)/g(theta)

    field = trapezoid_integral(integrable_func, 0, 2*pi, err)
    return I*field


def trapezoid_integral(f, a, b, h):
    return h * (f(a)/2 + f(b)/2 + sum([f(a+(j*h)) for j in range(1, int((b-a)/h))]))


def adaptive_trapezoidal(f, a, b, delta):
    h = .001
    n = (b-a)/h
    I_1 = trapezoid_integral(f, a, b, h)
    err = array([1000])
    while err.all() > delta:
        h /= 2
        n *= 2
        next_int = I_1/2 + h*(sum([f(a+k*h) for k in range(1, int(n), 2)]))
        err = abs(next_int - I_1)/3
        if err.any() < delta:
            return next_int, err
        else:
            I_1 = next_int


print("Magnetic field at (x,y,z)=(1,2,5) (calculated with adaptive method): ",
      adaptive_integrated_field(1, 2, 5, 1, .0001))


print("Now, we will create a density plot of this information, using (x,y,z)=(x,y,1) (THIS IS SLOW)")
dplot = zeros([100, 100])

i = 0
for x in linspace(-5, 5, 100):
    j = 0
    for y in linspace(-5, 5, 100):
        z = integrated_field(x, y, 1, 1)
        dplot[j][i] = sqrt(z.dot(z))
        j += 1
    i += 1


imshow(dplot)
show()
