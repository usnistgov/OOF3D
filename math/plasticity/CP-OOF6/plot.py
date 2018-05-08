# Crystal Plasticity Code.

import math,sys
from pylab import *



#---------------- reading input file -------------------- 
f = open('SS22.txt','r')
nstep = sum(1 for _ in f)
f.close()

f = open('SS22.txt','r')
ss = []
ssx = []
ssy = []

for i in range(nstep):
    ss.append([float(x) for x in f.readline().split()])

for i in range(nstep):
    ssx.append(ss[i][0])
    ssy.append(ss[i][1])
    

plot(ssx,ssy)
ylabel('Stress(MPa)')
xlabel('Strain')

show()

f.close()
