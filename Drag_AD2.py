# Detailed Drag Estimation in Aircraft Design 2

import math
import constants as con
import wing_area as wa

# fuselage drag estimation (page 12 in pdf)

Re = 11 # reynolds number
C_Ftu = 0.455 / (math.log10(Re))**2.58 # friction coefficient turbulent flow

d_f = 0.5 * (con.bf + con.hf) # averaged diameter of the fuselage
l_f = con.l_fus_s # length fuselage
k_f = 2.2 * (d_f / l_f)**1.5 + 3.8 * (d_f / l_f)**3 # pressure drag factor
k_lgb = 1/5 * k_f # penalty factor for the landing gear boxes 

S_w = wa.wing_area_s() # wing area
S_fwet = con.SG
c_Df = C_Ftu * (1 + k_f + k_lgb) * S_fwet / S_w # Fuselage Drag Coefficient