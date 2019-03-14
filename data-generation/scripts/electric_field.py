print("Problem 5.21: Electric Field")
from math import *
from numpy import *
from pylab import*

eps0 = 8.854187817e-12
q1, q2 = 1, -1
dist = 0.1  # between charges [m]
prefac = 4 * pi * eps0


num = 100  # Num grid pts , 1cm per sq
xMin, xMax, yMin, yMax = 0, 1, 0, 1
hx, hy = (xMax - xMin) / num, (yMax - yMin) / num
x, y = arange(xMin, xMax + hx, hx), arange(yMin, yMax + hy, hy)
8
r1 = zeros([num, num], float)
r2 = copy(r1)

x1, y1 = xMax / 2 + dist / 2, yMax / 2
x2, y2 = xMax / 2 - dist / 2, yMax / 2

phi = copy(r2)
for i in range(num):
    for j in range(num):
        r1[i, j] = sqrt((x[i] - x1)**2 + (y[j] - y1)**2)
        r2[i, j] = sqrt((x[i] - x2)**2 + (y[j] - y2)**2)
        phi[i, j] = q1 / (prefac * r1[i, j]) + q2 / (prefac * r2[i, j])

plt.imshow(phi, origin='lower ', extent=[xMin, xMax, yMin, yMax])
plt.xlabel('$x$ $[m]$')
plt.ylabel('$y$ $[m]$')
plt.show()


print("P. 5.21 B Starts Here")

numCharges = 5
q = array([1, 1, 1, 1, 1])  # charge on point charges
num = 100  # num grid pts per axis xMin, xMax, yMin, yMax = 0, 1, 0, 1
h = array([(xMax - xMin) / num, (yMax - yMin) / num])
x, y = arange(xMin, xMax + h[0], h[0]), arange(yMin, yMax + h[1], h[1])

# r stores distance of grid point from each charge
r = zeros([num, num, numCharges], float)

phi = zeros([num, num], float)
phix, phiy = copy(phi), copy(phi)
magE = zeros([num, num], float)
thetaE = copy(magE)

# rCharge stores positions of charges . Note it ’s best to
# place charges off−grid to avoid numerical issues as r−>0
rCharge = zeros([2, numCharges], float)
for k in range(numCharges):
    rCharge[0, k], rCharge[1, k] = xMax / 2 - \
        2 * dist + dist * k + h[0] / 2, yMax / 2

for k in range(numCharges):
    for i in range(num):
        for j in range(num):
            r[i, j, k] = sqrt((x[i] - rCharge[0, k])**2 +
                              (y[j] - rCharge[1, k])**2)
            phi[i, j] += q[k] / (prefac * r[i, j, k])
    print(k)

# Find derivatives , get E−field info :
for i in range(num):
    for j in range(num):
        if i != 0 and i != num - 1 and j != 0 and j != num - 1:
            phix[i, j] = (phi[i + 1, j] - phi[i - 1, j]) / (2 * h[0])
            phiy[i, j] = (phi[i, j + 1] - phi[i, j - 1]) / (2 * h[1])
            magE[i, j] = sqrt(phix[i, j]**2 + phiy[i, j]**2)
            thetaE[i, j] = arctan((-phiy[i, j] / magE[i, j]) /
                                  (-phix[i, j] / magE[i, j]))


imshow(magE, origin='lower', extent=[xMin, xMax, yMin, yMax])
plt.xlabel('$x$ $[m]$', fontsize=20)
plt.ylabel('$y$ $[m]$', fontsize=20)
plt .show()

fig, ax = plt.subplots()
cax = ax.imshow(thetaE, origin='lower', extent=[
                xMin, xMax, yMin, yMax], cmap=cm.hsv)
tMin, tMax = 0, 2 * pi
cbar = fig.colorbar(cax, ticks=[-1.56, 0, 1.56])
cbar.ax.set_yticklabels(['0', r"$\pi$", r'$2\pi$'])
cbar.set_label(r'$\Theta$ $[\mathrm{rad}]$', fontsize=18)
plt.xlabel('$x$ $[m]$', fontsize=20)
plt.ylabel('$y$ $[m]$', fontsize=20)
plt.show()
