# Problem 1
"""
Our ability to resolve detail in astronomical observations is limited by the diffraction of light in our telescopes. Light from stars can be treated effectively as coming from a point source at infinity. When such light, with wavelength λ, passes through the circular aperture of a telescope (which we’ll assume to have unit radius) and is focused by the telescope in the focal plane, it produces not a single dot, but a circular diffraction pattern consisting of central spot surrounded by a series of concentric rings. The intensity of the light in this diffraction pattern is given by ............
"""

from numpy import cos, sin, pi
from pylab import *


def f(theta, m):
    return cos(m*theta - x*sin(theta))


def J(m, x):
    N = 1000
    a = 0.
    b = pi
    h = (b-a)/N

    s = f(a, m) + f(b, m) + 4*f(b-h, m)
    for k in range(1, N//2):
        s += 4*f(a + (2*k-1)*h, m) + 2*f(a+2*k*h, m)
    I = h/3*s/pi
    return I


x = linspace(0, 20)

plot(x, J(0, x), label='J0')
plot(x, J(1, x), label='J1')
plot(x, J(2, x), label='J2')
legend()
show()


print("NOW DOING THE DENSITY PLOT: 5.4B")

x, y = mgrid[-1:1:100j, -1:1:100j]
r = sqrt(x**2 + y**2)
wavelength = 0.5
k = 2*pi/wavelength

I = (J(1, r*k)/k/r)**2
imshow(I, vmax=0.1/10, extent=(-1, 1, -1, 1))
show()

print("DONE WITH EX. 5.4")
