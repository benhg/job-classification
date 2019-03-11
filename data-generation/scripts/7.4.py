#!/usr/bin/python
import numpy as np
import pylab


def part_a():
    data = np.loadtxt('dow.txt')
    pylab.plot(data)
    pylab.show()


def part_b():
    data = np.loadtxt('dow.txt')
    fft = np.fft.rfft(data)
    pylab.plot(fft)
    pylab.show()


def part_c():
    data = np.loadtxt('dow.txt')
    fft = np.fft.rfft(data)
    fft[int(len(fft)*0.1):] = [0] * (len(fft) - int(len(fft)*0.1))
    pylab.plot(fft)
    pylab.show()


def part_d():
    data = np.loadtxt('dow.txt')
    fft = np.fft.rfft(data)
    fft[int(len(fft)*0.1):] = [0] * (len(fft) - int(len(fft)*0.1))
    new_data = np.fft.irfft(fft)
    pylab.plot(data)
    pylab.plot(new_data)
    pylab.show()


def part_e():
    data = np.loadtxt('dow.txt')
    fft = np.fft.rfft(data)
    fft[int(len(fft)*0.02):] = [0] * (len(fft) - int(len(fft)*0.02))
    new_data = np.fft.irfft(fft)
    pylab.plot(data)
    pylab.plot(new_data)
    pylab.show()


def main():
    # part_a()
    # part_b()
    part_c()
    part_d()
    part_e()


if __name__ == "__main__":
    main()
