from consts import *


#thetaGTab is an array, k=0,1,...,N-1
#q=0,1,...,Q
thetaGTab=[]
for k in range(0,N):
    thetaGTab.append(list(np.arange(0,Q+1)))

#y0 is a vector of each y0k,k=0,1,...,N-1
y0=[]

#H1 is a vector of each H1k, k=0,1,...,N-1
H1Vec=[]

#beta is an array, q=0,1,...,Q
#k=0,1,...,N-2
beta=[]
for q in range(0,Q+1):
    beta.append(list(np.arange(0,N-1)))


W=[]
