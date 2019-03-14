# Exercise 6.9

from math import*
from numpy import linspace
from numpy.linalg import*
from pylab import *
import scipy.integrate

L = 5 * 10**-10
a = 10 * 1.6 * 10**-19
hbar = 1.05 * 10**-34
mass = 9.1 * 10**-31


def simpson(f, a, b, h):

    n = int(abs(b - a) / h)
    if n % 2 != 0:
        n -= 1

    sum1 = 0
    s3 = 0
    for i in range(1, n, 2):
        s3 += f(a + (i * h))
    s3 *= 4
    sum1 += s3
    sum2 = 0
    s4 = 0
    for i in range(2, n - 1, 2):
        s4 += f(a + i * h)
    s4 *= 2
    sum2 = s4
    approx = h / (3.0) * (f(a) + f(b) + sum1 + sum2)
    return approx


def V(x):
    return (a / L) * x


def Hmn(m, n, V):
    return (2 / L) * simpson(lambda x: sin(m * pi * x / L) * ((n**2 * pi**2 * hbar**2 /
                                                               (2 * mass * L**2)) * sin(n * pi * x / L) + V(x) * sin(n * pi * x / L)), 0, L, .01 * L)


H = zeros([20, 20], float)
for m in range(0, 20):
    for n in range(0, 20):
        H[m][n] = Hmn(m + 1, n + 1, V)


energy, Anp = eigh(H)
energy *= 6.2 * 10**18

# -----------------------------------------------------------------------------------------------


def phi(n, x):
    return sqrt(2 / L) * sin(n * pi * x / L)


def generate_psi(phi, col):
    return lambda x: sum(col[sam] * phi(sam, x)
                         for sam in list(range(len(col))))


psis = []
for vec in Anp:
    psis.append(generate_psi(phi, vec))


def check_symmetric(a, tol=1e-8):
    return allclose(a, a.T, atol=tol)


print(("H is symmetric?: {}".format(check_symmetric(H))))

print("Problem 6.9 D. Recomputing H to dimension 100x100. This solution is pretty close to the one we had before. This suggests the old one may be good enough.")
H = zeros([100, 100], float)
for m in range(0, 100):
    for n in range(0, 100):
        H[m][n] = Hmn(m + 1, n + 1, V)


energy, Anp = eigh(H)
print((hbar / energy[1]))
energy *= 6.2 * 10**18


print("Additional problem from Mohamed starts here.")


def An(x, n):
    if 0 <= x < L / 2:
        return sqrt(12 / L**3) * simpson(lambda x: x *
                                         psis[n](x), 0, L / 2, .01 * L)
    elif L / 2 <= x <= L:
        return sqrt(12 / L**3) * simpson(lambda x: (L - x)
                                         * psis[n](x), L / 2, L, .01 * L)
    else:
        print("x Out of Bounds")
        return


def An(x, n):
    return sqrt(12 / L**3) * simpson(lambda x: x * psis[n](x), 0, L / 2, .01 * L) + sqrt(
        12 / L**3) * simpson(lambda x: (L - x) * psis[n](x), L / 2, L, .01 * L)


def Psi(x, t):
    return sum([An(x, n) * estuff(t, n) * psis[n](x)
                for n in range(len(psis))])


def estuff(t, n):
    return e ** (-(0 + 1j) * energy[n] * t * (1 / hbar))


print("this movie takes forever to generate. feel free to wait, but there's also a precomputed one in the folder, saved as 'psis.html'")

img = []
NUM_FRAMES = 100


def generate(t):
    ans = [abs(Psi(x, t))**2 for x in linspace(0, L, 100)]
    #img.append(plot(linspace(0, L, 100), ans, label="$\Psi(x, t=%s)$" % t))
    integ = scipy.integrate.simps(ans, linspace(0, L, 100))
    print(integ)

    print(("Psi_{}".format(i + 1)))
    # plt.savefig(
    #    "psis_frames/frame{}.png".format(str(i+1).zfill(7)))
    # clf()


import multiprocessing
pool = multiprocessing.Pool(12)

i = 0

pool.map(generate, linspace(0, 1.1269939220108039e-16, NUM_FRAMES))
i += 1
