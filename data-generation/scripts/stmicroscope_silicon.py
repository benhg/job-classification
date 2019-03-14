from numpy import *
from pylab import *
from math import *
import scipy
from scipy import ndimage


def load_file(path):
    """Read altitude or stm file data"""
    with open(path) as fh:
        w = []
        i = 0
        for line in fh:
            ln = []
            for word in line.split(" "):
                try:
                    ln.append(float(word.strip()))
                except ValueError as e:
                    print(word)
            w.append(ln)
        return w


def w(x, y, data):
    """Define a function to help us access W data for a specific file"""
    return data[x][y]


def dwdx(x, y, h, data):
    """Partial W over Partial X"""
    return (w(x, y, data) + w(x + 1, y, data)) / h


def dwdy(x, y, h, data):
    """Partial W over Partial Y"""
    return (w(x, y, data) + w(x, y + 1, data)) / h


def I(x, y, phi, h, data):
    return ((cos(phi) * dwdx(x, y, h, data)) + (sin(phi) * dwdy(x, y, h, data))
            ) / (sqrt((dwdx(x, y, h, data))**2 + (dwdy(x, y, h, data))**2 + 1))


print("""Loading in STM data and plotting it""")
dat = load_file("stm.txt")
PHI = pi / 4
H_dat = 250

d_plot = zeros([len(dat), len(dat[0])])
for i, val in enumerate(copy(dat)):
    for j, val2 in enumerate(val):
        try:
            d_plot[i][j] = I(i, j, PHI, H_dat, dat)
        except IndexError as e:
            pass


gray()
imshow(d_plot, origin="upper")
show()
