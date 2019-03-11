from pylab import *
from numpy import *
import numpy as np

GMs = 4*pi**2
CORR = 0


def f1(x, y, vx, vy, t):
    return vx


def f2(x, y, vx, vy, t):
    return vy


def f3(x, y, vx, vy, t, GAMMA):
    return -(GMs*x)/((x**2+y**2)**(3/2+CORR))*(1 + (GAMMA)/(x**2+y**2))


def f4(x, y, vx, vy, t, GAMMA):
    return -(GMs*y)/((x**2+y**2)**(3/2+CORR))*(1 + (GAMMA)/(x**2+y**2))


def solar_system_rk4(r0, v0, f1, f2, f3, f4, tmax, gamma):

    xpts = []
    ypts = []
    vxpts = []
    vypts = []
    h = .00001
    x = r0
    y = 0
    vx = 0
    vy = v0
    tpoints = arange(0, tmax, h)
    for t in tpoints:
        k1 = h*f1(x, y, vx, vy, t)
        l1 = h*f2(x, y, vx, vy, t)
        m1 = h*f3(x, y, vx, vy, t, gamma)
        n1 = h*f4(x, y, vx, vy, t, gamma)
        k2 = h*f1(x + k1/2, y+l1/2, vx+m1/2, vy+n1/2, t+h/2)
        l2 = h*f2(x + k1/2, y+l1/2, vx+m1/2, vy+n1/2, t+h/2)
        m2 = h*f3(x + k1/2, y+l1/2, vx+m1/2, vy+n1/2, t+h/2, gamma)
        n2 = h*f4(x + k1/2, y+l1/2, vx+m1/2, vy+n1/2, t+h/2, gamma)
        k3 = h*f1(x + k2/2, y+l2/2, vx+m2/2, vy+n2/2, t+h/2)
        l3 = h*f2(x + k2/2, y+l2/2, vx+m2/2, vy+n2/2, t+h/2)
        m3 = h*f3(x + k2/2, y+l2/2, vx+m2/2, vy+n2/2, t+h/2, gamma)
        n3 = h*f4(x + k2/2, y+l2/2, vx+m2/2, vy+n2/2, t+h/2, gamma)
        k4 = h*f1(x + k3, y+l3, vx+m3, vy+n3, t+h)
        l4 = h*f2(x + k3, y+l3, vx+m3, vy+n3, t+h)
        m4 = h*f3(x + k3, y+l3, vx+m3, vy+n3, t+h, gamma)
        n4 = h*f4(x + k3, y+l3, vx+m3, vy+n3, t+h, gamma)
        x = x + 1/6 * (k1 + 2 * k2 + 2*k3 + k4)
        y = y + 1/6 * (l1 + 2 * l2 + 2*l3 + l4)
        vx = vx + 1/6 * (m1 + 2 * m2 + 2*m3 + m4)
        vy = vy + 1/6 * (n1 + 2 * n2 + 2*n3 + n4)
        xpts.append(x)
        ypts.append(y)
        vxpts.append(vx)
        vypts.append(vy)

    return xpts, ypts, vxpts, vypts, tpoints


def get_vmin(alpha):
    xpts, ypts, vxpts, vypts, tpts = solar_system_rk4(
        .3897, 8.166, f1, f2, f3, f4, 1, alpha)
    vs = []
    thetas = []
    for i in range(len(xpts)):
        vs.append(sqrt(vxpts[i]**2 + vypts[i]**2))
        thetas.append(arctan2(ypts[i], xpts[i]))
    return vs, thetas, xpts, ypts, tpts


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), int(n)):
        yield l[i:i + int(n)]


def get_mean(alpha):
    vs, thetas, xpts, ypts, tpts = get_vmin(alpha)
    rpts = []
    for i, x in enumerate(xpts):
        rpts.append(sqrt(x**2 + ypts[i]**2))
    maxs = [vs.index(max(x)) for x in chunks(vs, len(vs)/7)][:-1]
    dts = []
    for j, i in enumerate(maxs):
        try:
            time = tpts[i]
            tnext = tpts[i+1]
            dts.append((thetas[i+1] - thetas[i])/(tnext - time))
        except:
            pass
    plot(tpts, vs)
    plot([tpts[i] for i in maxs], [vs[i] for i in maxs], "ok")
    return mean(dts)


import multiprocessing
alphas = linspace(.0001, .001, 100)
pool = multiprocessing.Pool()
means = pool.map(get_mean, alphas)


from scipy import stats

plot(alphas, means)

mercury_alpha = .0001
slope, intercept, r_value, p_value, std_err = stats.linregress(alphas, means)
print("Mercury's Perihelion processes at a rate of ",
      ((slope * mercury_alpha) + intercept)/2)
