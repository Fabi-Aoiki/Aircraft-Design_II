# Detailed Drag Estimation in Aircraft Design 2

import math
import constants as con
import wing_area as wa
import Drag_Estimation as DE
import isa

# fuselage drag estimation (page 12 in pdf)

l_f = con.l_fus_s # length fuselage
v_cruise = con.ma_stretch * isa.isa_model(con.H_CRUISE, con.dt)[3] #cruise speed in m/s
Re = DE.reynoldsCalc(v_cruise, l_f) # reynolds number
C_Ftu = 0.455 / (math.log10(Re))**2.58 # friction coefficient turbulent flow

d_f = 0.5 * (con.bf + con.hf) # averaged diameter of the fuselage

k_f = 2.2 * (d_f / l_f)**1.5 + 3.8 * (d_f / l_f)**3 # pressure drag factor
k_lgb = 1/5 * k_f # penalty factor for the landing gear boxes 

S_w = wa.wing_area_s() # wing area
S_fwet = con.SG # fuselage wetted area (might need to be updated due to new landing gear pods)
c_Df = C_Ftu * (1 + k_f + k_lgb) * S_fwet / S_w # fuselage drag coefficient


# nacelle drag estimation (page 13 in pdf)

l_n = 2 # length nacelle (meters)
v_cruise = con.ma_stretch * isa.isa_model(con.H_CRUISE, con.dt)[3] #cruise speed in m/s
Re = DE.reynoldsCalc(v_cruise, l_n) # reynolds number
C_Ftu = 0.455 / (math.log10(Re))**2.58 # friction coefficient turbulent flow

d_n = 1.2 # diameter nacelle (meters)
k_n = 2.2 * (d_n / l_n)**1.5 + 3.8 * (d_n / l_n)**3 # pressure drag factor

S_nwet = d_n**2 * 3.1416 / 4 * l_n * con.N_E # wetted surface of all four nacelles
c_Dn = C_Ftu * (1 + k_f) * S_nwet / S_w # fuselage drag coefficient


# compressible drag estimation (page 11 in pdf)

phi_25 = 21.4 * 3.1416 / 180 # sweep angle quarter cord
M_dd = 0.758 # drag divergence Mach number
M_inf = con.ma_stretch 

DeltaM = M_inf - M_dd / math.sqrt(math.cos(phi_25))
DeltaC_D = 0.002 * math.exp(60 * DeltaM)