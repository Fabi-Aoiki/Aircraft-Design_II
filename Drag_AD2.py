# Detailed Drag Estimation in Aircraft Design 2

import math

# Fuselage Drag Estimation (page 12 in PDF)


C_Ftu = 0.455 / (math.log10(Re))**2.58 # Friction Coefficient Turbulent Flow

k_f = 2.2 * (d_f / l_f)**1.5 + 3.8 * (d_f / l_f)**3 # Pressure Drag Factor
k_lgb = 0 # penalty factor for the landing gear boxes 

c_Df = C_Ftu * (1 + k_f + k_lgb) * S_fwet / S_w # Fuselage Drag Coefficient