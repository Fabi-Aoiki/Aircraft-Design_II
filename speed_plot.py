import matplotlib.pyplot as plt
import numpy as np
from isa import isa_model


datenpunkte = 500
hList = []
vList = []
vcList = []
vdList = []
machCList = []
machDList = []
vCEAS = 330*1.852/3.6
MC = 0.8
vDEAS = 390*1.852/3.6
MD = MC+0.05

def calc_TAS(v_EAS,h):
    return v_EAS/(np.sqrt(isa_model(h,0)[2]/isa_model(0,0)[2]))

def calc_mach(mach,h):
    mach1 = isa_model(h,0)[3]
    return mach*mach1

for i in range(0, datenpunkte - 1):
    h = 14000 / datenpunkte * (i +1)
    hList.append(h)
    vcList.append(calc_TAS(vCEAS,h))
    vdList.append(calc_TAS(vDEAS,h))
    machCList.append(calc_mach(MC,h))
    machDList.append(calc_mach(MD,h))

xc = np.array(vcList)
xd = np.array(vdList)
y = np.array(hList)
xmc = np.array(machCList)
xmd = np.array(machDList)

plt.plot(xc,y,color = 'blue')
plt.plot(xmc,y, color = 'blue',linestyle='dashed')
plt.plot(xd,y,color = 'red')
plt.plot(xmd,y,color = 'red',linestyle='dashed')
plt.xlabel('vTAS [m/s]')
plt.ylabel('height [m]')
plt.legend(['vC,EAS = 154 m/s','MC = 0.8','vD,EAS = 200 m/s','MD = 0.85'])
plt.grid()
plt.show()
