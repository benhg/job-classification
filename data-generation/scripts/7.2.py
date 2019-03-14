#!/usr/bin/python
import numpy as np
import pylab


def dft(y):
    N = len(y)
    c = np.zeros(N // 2 + 1, complex)
    for k in range(N // 2 + 1):
        for n in range(N):
            c[k] += y[n] * np.exp(-2j * np.pi * k * n / N)
    return c


def part_a():
    data = np.loadtxt('sunspots.txt')
    print(("approx: {}".format(133.2)))
    pylab.plot(data[:, 0], data[:, 1])
    pylab.show()


def part_b():
    data = np.loadtxt('sunspots.txt')
    coef = np.fft.rfft(data[:, 1])
    pylab.plot(np.power(np.abs(coef), 2))
    pylab.show()


def part_c():
    data = np.loadtxt('sunspots.txt')
    coef = list(np.fft.rfft(data[:, 1]))
    disp = [np.abs(x)**2 for x in coef]
    peak = disp.index(max(disp[2:]))
    print((coef[24]))


def main():
    part_a()
    part_b()
    part_c()


if __name__ == "__main__":
    main()
