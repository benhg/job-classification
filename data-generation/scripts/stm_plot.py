



_ = eval(input("Press any key when ready to continue"))
from numpy import *
from pylab import *

data = loadtxt('stm.txt')
gray()
imshow(data)
xlim(0, 650)
ylim(0, 650)
show()

