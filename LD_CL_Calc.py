import numpy as np
import constants as con
import pandas as pd
import math
import isa as isa
from wing_area import wing_area_s

def Calc_LD():
        for h in np.linspace(0, 12000, 7):
                rho = isa.isa_model(h,0)[2] 
                a = isa.isa_model(h,0)[3]


                for M in np.linspace(0.1, 0.8, 8):
                        V=M*a
                        x = 2*(con.Wto_stretch*0.99) / (rho*(wing_area_s())*(V**2)) #x = CL
                        y = -127.06*x^6 + 214.11*x^5 + 71.803*x^4 - 236.72 * x^3 - 2.0649*x^2 + 104.22*x # y = L/D






















