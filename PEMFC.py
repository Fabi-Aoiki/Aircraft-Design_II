import numpy as np
import isa as isa
import constants as con
import math
############################################################# Value
#Basic Thermodynamic things

cp = (con.PEMFC_Kappa*con.PEMFC_R_s)/(con.PEMFC_Kappa-1)

#Changig values
h = []
TS0 = []
PS0 = []
M0 = []
q0 = []
PT0 = []
n=1
while n < con.H_CRUISE:
    h.append(n)
    n = n +1 

n=0
while n < con.ma_max:
    M0.append(n)
    n = n +0.01

for z in M0:
    TS0it = []
    PS0it = []
    PT0it = []
    qit = []
    for i in h:
        TS0it.append(isa.isa_model(i,con.dt)[1])
        PS0it.append(isa.isa_model(i,con.dt)[0])
        qit.append(((((isa.isa_model(i,con.dt)[3])*z)**2)*(isa.isa_model(i,con.dt)[2]))/2)
        PT0it.append(qit*PS0it)
    TS0.append(TS0it)
    PS0.append(PS0it)
    q0.append(qit)



    


#Values From Changing values
TT0 = []
for i in TS0:
    TT0 = i * (1+(((con.PEMFC_Kappa-1)/2)*(M0**2)))
