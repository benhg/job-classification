#!/usr/bin/python
import numpy as np
import pylab

def dct(y):
    N = len(y)
    y2 = np.empty(2*N,float)
    y2[:N] = y[:]
    y2[N:] = y[::-1]

    c = np.fft.rfft(y2)
    phi = np.exp(-1j*np.pi*np.arange(N)/(2*N))
    return np.real(phi*c[:N])

def idct(a):
    N = len(a)
    c = np.empty(N+1,complex)

    phi = np.exp(1j*np.pi*np.arange(N)/(2*N))
    c[:N] = phi*a
    c[N] = 0.0
    return np.fft.irfft(c)[:N]

def part_a():
    data = np.loadtxt('dow2.txt')
    fft = np.fft.rfft(data)
    fft[int(len(fft)*0.02):] = [0] * (len(fft) - int(len(fft)*0.02))
    new_data = np.fft.irfft(fft)
    pylab.plot(data)
    pylab.plot(new_data)
    pylab.show()

def part_b():
    data = np.loadtxt('dow2.txt')
    fft = dct(data)
    fft[int(len(fft)*0.02):] = [0] * (len(fft) - int(len(fft)*0.02))
    new_data = idct(fft)
    pylab.plot(data)
    pylab.plot(new_data)
    pylab.show()

def main():
    part_a()
    part_b()

if __name__ == "__main__":
    main()
