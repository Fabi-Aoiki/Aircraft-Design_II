import numpy as np
import constants as con
import isa as isa
#from Drag_AD2 import S_nwet
from wing_area import wing_area_s
import matplotlib.pyplot as plt
import Drag_Estimation as DE
import math


#################################################################################
#W O R K   I N   P R O G R E S S#
#################################################################################

def CalcAnaDrag(M,h):
        # fuselage drag estimation (page 12 in pdf)

        l_f = con.l_fus_s # length fuselage
        vel = M * isa.isa_model(h, con.dt)[3] #cruise speed in m/s
        Re = vel*l_f/isa.isa_model(h ,con.dt)[5] # Reynolds number
        C_Ftu = 0.455 / (math.log10(Re))**2.58 # friction coefficient turbulent flow
        d_f = 0.5 * (con.bf + con.hf) # averaged diameter of the fuselage
        k_f = 2.2 * (d_f / l_f)**1.5 + 3.8 * (d_f / l_f)**3 # pressure drag factor
        k_lgb = 1/5 * k_f # penalty factor for the landing gear boxes 
        S_w = wing_area_s() # wing area
        S_fwet = con.SG # fuselage wetted area (might need to be updated due to new landing gear pods)
        c_Df = C_Ftu * (1 + k_f + k_lgb) * S_fwet / S_w # fuselage drag coefficient

        # nacelle drag estimation (page 13 in pdf)

        l_n = 2 # length nacelle (meters)
        Re = vel*l_f/isa.isa_model(h ,con.dt)[5] # Reynolds number
        C_Ftu = 0.455 / (math.log10(Re))**2.58 # friction coefficient turbulent flow
        d_n = 1.2 # diameter nacelle (meters)
        k_n = 2.2 * (d_n / l_n)**1.5 + 3.8 * (d_n / l_n)**3 # pressure drag factor
        S_nwet = (d_n**2 * 3.1416 / 4 + d_n * 3.1416 * l_n) * con.N_E # wetted surface of all four nacelles
        c_Dn = C_Ftu * (1 + k_f) * S_nwet / S_w # fuselage drag coefficient

        # compressible drag estimation (page 11 in pdf)

        DeltaC_D = 0.0 # for M = 0.6
        
        return(c_Df + c_Dn + DeltaC_D)


def Calc_LD():
        for h in np.linspace(0, 12000, 7):
                rho = isa.isa_model(h,0)[2] 
                a = isa.isa_model(h,0)[3]

                CL_list = []
                LD_list = []

                for M in np.linspace(0.1, 0.8, 80):

                        V=M*a
                        x = 2*(con.Wto_stretch*0.99) / (rho*(wing_area_s())*(V**2)) #x = CL
                        #v_cl = np.sqrt(2*con.Wto_stretch*0.99/(rho*197.5)*cl)
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

                # Adding analytical drags
                DeltaD = CalcAnaDrag(0.6, h)
                for i in range(len(LD)):
                        if LD[i] is not None and CL[i] is not None:
                                TotalD = 1/LD[i] * CL[i] + DeltaD
                                LD[i] = CL[i]/TotalD

                plt.plot(CL, LD, label = str(h) + " m")
        plt.xlabel("CL")
        plt.ylabel("CL/CD")
        plt.legend(loc='best')
        plt.grid(True)
        plt.show()
        plt.close()

def Calc_LD_M():
        for h in np.linspace(0, 12000, 7):
                rho = isa.isa_model(h,0)[2]
                a = isa.isa_model(h,0)[3]

                M_list = []
                LD_list = []
                CL_list = []

                for cl in np.linspace(0.1, 2, 80):

                        #V=M*a
                        #x = 2*(con.Wto_stretch*0.99) / (rho*(wing_area_s())*(V**2)) #x = CL
                        v = np.sqrt(2*con.Wto_stretch*0.99/(rho*197.5)*cl)
                        M=v/a
                        x=cl
                        CL_list.append(cl)
                        if x>1.07:

                                x = None

                        M_list.append(M)
                        if x == None:
                                y = None
                        else:
                                y = -127.06 * x**6 + 214.11 * x**5 + 71.803 * x**4 - 236.72 * x**3 - 2.0649 * x**2 + 104.22 * x # y = L/D
                        LD_list.append(y)
                        print(x,y)

                Mach = np.array(M_list)
                LD = np.array(LD_list)
                CL = np.array(CL_list)

                # Adding analytical drags
                DeltaD = CalcAnaDrag(0.6, h)
                for i in range(len(LD)):
                        if LD[i] is not None and CL[i] is not None:
                                TotalD = 1/LD[i] * CL[i] + DeltaD
                                LD[i] = CL[i]/TotalD

                plt.plot(Mach, LD, label = str(h) + " m")
        plt.xlabel("Mach")
        plt.ylabel("CL/CD")
        plt.legend(loc='best')
        plt.grid(True)
        plt.show()
        plt.close()


Calc_LD()
Calc_LD_M()





















