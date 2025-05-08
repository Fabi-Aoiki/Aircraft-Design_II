import math
import numpy as np
import constants as cons
import isa

'''
def wing_area(W_TO,WS):
    return round(W_TO/WS,2)

def cl_cruise(WS, M):
    return round(2*cons.k_r*WS/(isa.gamma*isa.isa_model(cons.H_CRUISE,cons.dT_TO)[0]*M**2),4)

def buff_lim(cl):
    return round(cons.k_n * cons.k_av * cons.k_trim * cl,4)

def drag_div(cl):
    return round(cons.k_av * cons.k_trim * cl,4)

S = wing_area(cons.Wto,cons.WS_base)
cl_c = cl_cruise(cons.WS_base,cons.ma_max)
cl_BO = buff_lim(cl_c)
cl_DD = drag_div(cl_c)

print(isa.isa_model(cons.H_CRUISE,cons.dT_TO)[0])
print(S, cl_c, cl_BO, cl_DD)
'''
W_TO = cons.Wto
W_TO_stretch = cons.Wto_stretch
WS = cons.WS
#WS_base = 3700 #Test
#M = cons.ma_max
M = 0.79#Test
h_cruise = cons.H_CRUISE
dT = cons.dT_TO
phi_25 = 0
phi_25_deg = 0

def wing_area():
    W_TO = cons.Wto_stretch
    WS = cons.WS

    return round(W_TO/WS,2)

S = wing_area(W_TO,WS)
WS_stretch = round(W_TO_stretch/S,0)

def cl_cruise(WS, M):
    return round(2*cons.k_r*WS/(isa.gamma*isa.isa_model(h_cruise,dT)[0]*M**2),4)

def buff_lim(cl):
    cl_BO = round(cons.k_n * cons.k_av * cons.k_trim * cl, 6)
    M_n = round((-1)/8 * cl_BO + 0.875 ,3)
    return cl_BO, M_n

def drag_div(cl):
    cl_DD = round(cons.k_av * cons.k_trim * cl,4)
    M_drag_max = round(-0.1964*cl_DD**2+0.1494*cl_DD+0.7516,3) #Regression function drag-rise limit
    return cl_DD, M_drag_max

print(S)

cl_c_b = cl_cruise(WS,M)
cl_c_s = cl_cruise(WS_stretch,M)

cl_BO_b = buff_lim(cl_c_b)[0]
cl_BO_s = buff_lim(cl_c_s)[0]

M_n_b = buff_lim(cl_c_b)[1]
M_n_s = buff_lim(cl_c_s)[1]

cl_DD_b = drag_div(cl_c_b)[0]
cl_DD_s = drag_div(cl_c_s)[0]

M_drag_b = round(M_n_b/drag_div(cl_c_b)[1]*100,2)
M_drag_s = round(M_n_s/drag_div(cl_c_s)[1]*100,2)

#print(isa.isa_model(h_cruise,cons.dT_TO)[0])
print("Surface: ", S, "WS_stretch: ", WS_stretch,"; cl_c: ", cl_c_b,cl_c_s)
print("cl_BO: ", cl_BO_b, cl_BO_s,"; M_n approx.: ", M_n_b, M_n_s)
print("cl_DD: ", cl_DD_b, cl_DD_s, "; M_drag approx.: ", M_drag_b, M_drag_s)

if M_n_b < M:
    phi_25 = math.acos((M_n_b / M) ** 2)
    phi_25_deg = round(phi_25 / np.pi * 180, 1)

print("phi: ", phi_25_deg)

if M_n_s < M_n_b:
    print("Profile Mach number of stretch variant lower!\nTherefore M_max for stretch must be lower!")
    M_max_s = M_n_s / math.sqrt(math.cos(phi_25))
    print(round(M_max_s,3))

def wing_parameter(AR, taper):
    S = wing_area(cons.Wto,cons.WS)
    b = math.sqrt(AR*S)
    chord_mean = S/b
    chord_root = 2*S/(b*(taper+1))
    chord_tip = taper*chord_root
    return b, chord_mean, chord_root, chord_tip, S
print(wing_parameter(cons.AR,cons.taper)[0],wing_parameter(cons.AR,cons.taper)[1],wing_parameter(cons.AR,cons.taper)[2], wing_parameter(cons.AR,cons.taper)[3])