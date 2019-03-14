#!/usr/bin/python
import numpy as np
import pylab


def gen_data():
    return [
        1 if np.floor(2 * x) % 2 == 0 else -1 for x in np.linspace(0, 1, 1000)
    ]


def main():
    data = gen_data()
    fft = np.fft.rfft(data)
    fft[10:] = [0] * (len(fft) - 10)
    new_data = np.fft.irfft(fft)
    pylab.plot(data)
    pylab.plot(new_data)
    pylab.show()


if __name__ == "__main__":
    main()
