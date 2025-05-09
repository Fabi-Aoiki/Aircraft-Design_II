import numpy as np
import constants as con
import pandas as pd
import math
import isa
# from Wing_thorenbeck import Clac_nult
# from Drag_Estimation import s_de
import constants as con
import empennage_dimensioning as emp

def Calc_W_tail():
    # nult = Clac_nult()
    # k_wt = con.k_wt
    # S_tail = s_de

    # W_tail = k_wt * (nult * S_tail**(2))**(0.75)
    # W_tail = W_tail * con.Cor_factor_Ttail


    S_h = emp.horizontal_wing_parameter()[0] # horizontal wing area
    S_v = emp.vertical_wing_parameter()[0] # vertical fin area

    funcHori = S_h**0.2 * con.vD / 1000 / (np.cos(con.Lambda_h * 3.1416/180))**0.5 # Figure 8.5 in Torenbeek
    funcVert = S_v**0.2 * con.vD / 1000 / (np.cos(con.Lambda_v * 3.1416/180))**0.5 # Figure 8.5 in Torenbeek
    # print("funcHori: " + str(funcHori) + "    " + "funcVerti: " + str(funcVert))
    
    if funcHori < 0.45 and funcVert < 0.45:
        funcHoriRes = 63.333 * funcHori - 3.333 # linear equation
        funcVertRes = 63.333 * funcVert - 3.333
    else:
        pass
        # funcHoriRes = 27 # manual input required from figure 8.5 (kg/m^2)
        # funcVertRes = 27 # manual input required from figure 8.5 (kg/m^2)

    k_h = 1.0 # fixed stabilizer

    h_h = emp.horizontal_wing_parameter()[1] # not sure if correct value
    b_v = emp.vertical_wing_parameter()[1]

    k_v = 1 + 0.15 * (S_h * h_h) / (S_v * b_v) # T-tail

    W_h = S_h * k_h * funcHoriRes # mass of horizontal tail wing (kg)
    W_v = S_v * k_v * funcVertRes # mass of vertical tail wing (kg)

    W_tail = W_h + W_v

    return(W_tail)

# W_tail = Calc_W_tail()
# print("W_tail: " + str(W_tail) + " kg")