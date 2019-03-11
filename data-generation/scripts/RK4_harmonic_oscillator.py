
# RK4 on a double differential eqn.
from numpy import arange
from pylab import *
l = 9.8
g = l
q = .5
fd = 1.5
Omega = 2/3


def f1(theta, omega, t):
    return omega


def f2(theta, omega, t):
    return -(g/l)*sin(theta) - q*omega + fd*sin(Omega * t)


def thetomega(theta0, omega0, f1, f2, time):

    theta = theta0
    omega = omega0

    thetapoints = []
    omegapoints = []
    tpoints = arange(0, time, .1)
    h = .1
    for t in tpoints:
        theta = theta - 2*pi if theta > pi else theta + 2*pi if theta < -1*pi else theta
        thetapoints.append(theta)
        omegapoints.append(omega)
        k1 = h * f1(theta, omega, t)
        l1 = h * f2(theta, omega, t)
        k2 = h*f1(theta+k1/2, omega+l1/2, t+h/2)
        l2 = h*f2(theta+k1/2, omega+l1/2, t+h/2)
        k3 = h*f1(theta+k2/2, omega+l2/2, t+h/2)
        l3 = h*f2(theta+k2/2, omega+l2/2, t+h/2)
        k4 = h*f1(theta+k3, omega+l3, t+h)
        l4 = h*f2(theta+k3, omega+l3, t+h)
        theta = theta + 1/6 * (k1 + 2*k2 + 2*k3 + k4)
        omega = omega + 1/6 * (l1 + 2*l2 + 2*l3 + l4)
    return thetapoints, omegapoints, tpoints


thetapoints, omegapoints, tpoints = thetomega(0.2, 0, f1, f2, 100)
t2, o2, tp2, =  thetomega(0.2+10**-6, 0, f1, f2, 1)
# plot(thetapoints, omegapoints)

plot(tpoints, thetapoints, label="$\Theta_0$ = 2")
plot(tp2, t2, label="$\Theta_0$ = 2 + $10^{-6}$")
legend()

#plot(tpoints, [log(abs(theta-t2[i])) for i, theta in enumerate(thetapoints)])

show()
