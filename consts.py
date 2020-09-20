import numpy as np

#fermion number
N=100
#k=0,1,...,N-1
kIndAll=range(0,N)
dk=2*np.pi/N

#before quench
mu0=0
t0=0.5
d0=-0.5

#after quench
mu1=-3
t1=t0
d1=d0

#time step number
Q=200

#time step
ds=0.05

tol=1e-15

cutOff=1.2
threadNum=12