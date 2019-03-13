import numpy as np
import matplotlib.pyplot as plt
soa =np.array( [ [0,0,4,3], [0,0,4,3],[0,0,2,-9]]) 
X,Y,U,V = list(zip(*soa))
plt.figure()
ax = plt.gca()
ax.quiver(X,Y,U,V,angles='xy',scale_units='xy',scale=1)
ax.set_xlim([-1,10])
ax.set_ylim([-1,10])
plt.draw()
plt.show()
