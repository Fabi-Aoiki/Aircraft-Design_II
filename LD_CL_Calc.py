import numpy as np
import constants as con
import isa as isa
from Drag_AD2 import S_nwet
from wing_area import wing_area_s
import matplotlib.pyplot as plt


#################################################################################
#W O R K   I N   P R O G R E S S#
#################################################################################


def Calc_LD():
        for h in np.linspace(0, 12000, 7):
                rho = isa.isa_model(h,0)[2] 
                a = isa.isa_model(h,0)[3]

                CL_list = []
                LD_list = []

                for M in np.linspace(0.1, 0.8, 80):

                        V=M*a
                        x = 2*(con.Wto_stretch*0.99) / (rho*(wing_area_s())*(V**2)) #x = CL
                        if x>1.07:

                                x = None

                        CL_list.append(x)
                        if x == None:
                                y = None
                        else:
                                y = -127.06 * x**6 + 214.11 * x**5 + 71.803 * x**4 - 236.72 * x**3 - 2.0649 * x**2 + 104.22 * x # y = L/D
                        LD_list.append(y)
                        print(x,y)

                CL = np.array(CL_list)
                LD = np.array(LD_list)

                plt.plot(CL, LD)
                plt.show()

Calc_LD()
























