from numpy import arange,empty, array,zeros
from pylab import *

class rksolve:
	
	def __init__(self,f):
		self.f = f
		self.initial_conditions = None
		self.solution = None
		
	def iterate(self,a,b,N=1000):
		
		f = self.f
		r0 = array(self.initial_conditions,float)
		
		h = (b-a)/N
		
		tpoints = arange(a,b,h)
		solution = empty(tpoints.shape + r0.shape,float)
		
		#r_points[0] = r0
		r = r0
		for i,t in enumerate(tpoints):
		    solution[i]=r
		    k1 = h*f(r,t)
		    k2 = h*f(r+0.5*k1,t+0.5*h)
		    k3 = h*f(r+0.5*k2,t+0.5*h)
		    k4 = h*f(r+k3,t+h)
		    r += (k1+2*k2+2*k3+k4)/6
		
		self.h = h
		self.solution = solution
		self.t = tpoints


k = 6
m = 1
omega = 2

def f(r,t):
	
	N = len(r)//2
	ksi = r[:N]
	vel = r[N:]
	
	D = empty(r.shape,float)
	Dksi = D[:N]
	Dvel = D[N:]
	# Lets assign velocities as position derivatives
	
	Dksi[:] = vel
	
	Dvel[0] = cos(omega*t)/m + k/m*(ksi[1]-ksi[0]) 
	Dvel[-1] = k/m*(ksi[-2]-ksi[-1])
	
	for i in range(1,N - 1):
		Dvel[i] = k/m*( (ksi[i+1]-ksi[i]) + (ksi[i-1] - ksi[i]) )
	
	return D
	
prob = rksolve(f)
N = 5
r0 = zeros(N*2,float)

prob.initial_conditions = r0
prob.iterate(0,20,1000)



for i in range(N):
	ksi_i = prob.solution[:,i]
	plot(prob.t,ksi_i,label=i)

legend()
show()
