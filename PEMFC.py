import numpy as np
import isa as isa
import constants as con
import math

#Basic Thermodynamic things

cp = (con.PEMFC_Kappa*con.PEMFC_R_s)/(con.PEMFC_Kappa-1)

#Changig values
h = []
TT0 = []
n=1
while n < con.H_CRUISE:
    h.append(n)
    n = n +1 

for i in h:
    TT0.append(isa.isa_model(i,con.dt)[1])
