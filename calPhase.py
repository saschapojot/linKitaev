from initDat import *
import scipy.linalg as slin
from multiprocessing import Pool
import matplotlib.pyplot as plt
from datetime import  datetime
def b0(k):
    return 2*d0*np.sin(k*dk)

def c0(k):
    return 2*t0*np.cos(k*dk)+mu0

def initVec(k):
    b0Val=b0(k)
    c0Val=c0(k)
    denom2=2*b0Val**2+2*c0Val**2-2*c0Val*np.sqrt(b0Val**2+c0Val**2)
    if denom2>tol:
        denom=np.sqrt(denom2)
        numer1=1j*b0Val
        numer2=c0Val-np.sqrt(b0Val**2+c0Val**2)
        return np.array([numer1/denom,numer2/denom])
    else:
        if c0Val>0:
            return np.array([1,0])
        else:
            return np.array([0,1])
def b1(k):
    return 2*d1*np.sin(k*dk)
def c1(k):
    return 2*t1*np.cos(k*dk)+mu1

def H1(k):
    b1Val=b1(k)
    c1Val=c1(k)
    h1Val=np.zeros((2,2),dtype=complex)
    h1Val[0,0]=-c1Val
    h1Val[0,1]=1j*b1Val
    h1Val[1,0]=-1j*b1Val
    h1Val[1,1]=c1Val
    return h1Val
#calculate all y0k s
for k in kIndAll:
    y0.append(initVec(k))
#calculate all H1k
for k in kIndAll:
    H1Vec.append(H1(k))

def thetaD(q,k):
    y0k=y0[k]
    h1Val=H1Vec[k]
    tmp=-np.conj(y0k.transpose()).dot(h1Val).dot(y0k)*q*ds

    return tmp

def thetaTot(q,k):
    y0k=y0[k]
    h1Val=H1Vec[k]
    expH1=np.matrix(slin.expm(-1j*h1Val*q*ds))

    tmp=np.array(np.conj(y0k.transpose()).dot(expH1).dot(y0k))[0][0]


    return -1j*np.log(tmp/np.abs(tmp))



def thetaG(q,k):
    return thetaTot(q,k)-thetaD(q,k)

def oneThetaG(qAndKOnePair):
    qVal=qAndKOnePair[0]
    kVal=qAndKOnePair[1]
    tGVal=thetaG(qVal,kVal)
    return [qVal,kVal,tGVal]
qAndKAll=[[qVal, kVal] for qVal in range(0,Q+1) for kVal in kIndAll]
pool1=Pool(threadNum)
qKtG=pool1.map(oneThetaG,qAndKAll)
pool1.close()
pool1.join()
for item in qKtG:
    qVal=item[0]
    kVal=item[1]
    tGVal=item[2]
    thetaGTab[kVal][qVal]=tGVal

def jumpDecision(incr):
    tmp=incr/np.pi
    if tmp>=cutOff:
        return incr-2*np.pi
    elif tmp<=-cutOff:
        return incr+2*np.pi
    else:
        return incr




for q in range(0,Q+1):
    for k in range(0,N-1):
        tmp=np.real(thetaGTab[k+1][q]-thetaGTab[k][q])
        beta[q][k]=jumpDecision(tmp)

for q in range(0,Q+1):
    tmp=0.0
    for k in range(0,int(N/2)):
        tmp+=beta[q][k]
    tmp/=2*np.pi

    W.append(tmp)

Ts=np.arange(0,Q+1)*ds
plt.figure()
plt.plot(Ts,W)
plt.yticks(np.arange(np.floor(min(W)),np.floor(max(W))+1))
plt.show()
plt.close()