# Detailed Drag Estimation in Aircraft Design 2

import math
import constants as con
import wing_area as wa
import Drag_Estimation as DE
import isa
import matplotlib.pyplot as plt

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

S_nwet = (d_n**2 * 3.1416 / 4 + d_n * 3.1416 * l_n) * con.N_E # wetted surface of all four nacelles
c_Dn = C_Ftu * (1 + k_f) * S_nwet / S_w # fuselage drag coefficient


# compressible drag estimation (page 11 in pdf)

phi_25 = 21.4 * 3.1416 / 180 # sweep angle quarter cord
M_dd = 0.758 # drag divergence Mach number
M_inf = con.ma_stretch 

DeltaM = M_inf - M_dd / math.sqrt(math.cos(phi_25))
DeltaC_D = 0.002 * math.exp(60 * DeltaM)


# diagram CL over CD

# read values

def ExtrParamTxt(filename, varname):
    var_values = []
    with open(filename, "r", encoding="utf-8") as f:
        # Header-Zeile suchen
        for line in f:
            cols = line.split()
            if varname in cols:
                idx = cols.index(varname)
                break
        # Restdaten auslesen
        for line in f:
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            vals = line.split()
            var_values.append(float(vals[idx]))
    return(var_values)

# plot CD0 (CD_viscous) wing

cd_visc_wing_list = ExtrParamTxt("Aircraft-Design_II/CD_visc_wing.txt", "CD_viscous")
cl_visc_wing_list = ExtrParamTxt("Aircraft-Design_II/CD_visc_wing.txt", "CL")

plt.plot(cd_visc_wing_list, cl_visc_wing_list, linestyle = "-", label = "Parasite Drag")

# plot CD0 (CD_viscous) wing + htp + vtp

cd_visc_all_list = ExtrParamTxt("Aircraft-Design_II/CD_visc_all.txt", "CD_viscous")
cl_visc_all_list = ExtrParamTxt("Aircraft-Design_II/CD_visc_all.txt", "CL")

plt.plot(cd_visc_all_list, cl_visc_all_list, linestyle = "-", label = "HTP + VTP (Par.)")

# add CD0 (CDn) nacelle

cd_nac_list = []
cl_nac_list = cl_visc_all_list
for i in range(len(cd_visc_all_list)):
    cd_nac_list.append(cd_visc_all_list[i] + c_Dn)

plt.plot(cd_nac_list, cl_nac_list, linestyle = "-", label = "Nacelle Drag")

# add CD0 (CDf) fuselage

cd_fus_list = []
cl_fus_list = cl_visc_all_list
for i in range(len(cd_visc_all_list)):
    cd_fus_list.append(cd_visc_all_list[i] + c_Df + c_Dn)

plt.plot(cd_fus_list, cl_fus_list, linestyle = "-", label = "Fuselage Drag")

# add CDi (CD_induced) wing

cd_indu_wing_list = ExtrParamTxt("Aircraft-Design_II/CD_indu_wing.txt", "CD_induced")
cl_indu_wing_list = ExtrParamTxt("Aircraft-Design_II/CD_indu_wing.txt", "CL")

for i in range(len(cd_indu_wing_list)):
    cd_indu_wing_list[i] = cd_indu_wing_list[i] + cd_fus_list[i]

plt.plot(cd_indu_wing_list, cl_indu_wing_list, linestyle = "-", label = "Induced Drag")

# add CDi (CD_induced) wing + htp + vtp

cd_indu_all_list = ExtrParamTxt("Aircraft-Design_II/CD_indu_all.txt", "CD_induced")
cl_indu_all_list = ExtrParamTxt("Aircraft-Design_II/CD_indu_all.txt", "CL")

for i in range(len(cd_indu_all_list)):
    cd_indu_all_list[i] = cd_indu_all_list[i] + cd_fus_list[i]

plt.plot(cd_indu_all_list, cl_indu_all_list, linestyle = "-", label = "Trim Drag")

# add Compr Drag

cd_compr_list = []
cl_compr_list = cl_indu_all_list
for i in range(len(cl_indu_all_list)):
    cd_compr_list.append(cd_indu_all_list[i] + DeltaC_D)

plt.plot(cd_compr_list, cl_compr_list, linestyle = "-", label = "Compr. Drag")

# plot everything

plt.xlim(0)
plt.xlabel("CD")
plt.ylabel("CL")
plt.legend(loc='best')
plt.grid(True)
plt.show()
plt.close()


# L/D vs CL for different flight altitudes

altitudes_list = [12000, 6000, 0]
v_list = [236, 210, 154] # m/s

# drag function for analytical expressions

def DragFactorsAlti(altitudes_list, v_list):

    c_Df_list = []
    for i in range(len(altitudes_list)):
        Re = DE.reynoldsCalc(v_list[i], l_f)
        C_Ftu = 0.455 / (math.log10(Re))**2.58 
        c_Df = C_Ftu * (1 + k_f + k_lgb) * S_fwet / S_w
        c_Df_list.append(c_Df)
    
    c_Dn_list = []
    for i in range(len(altitudes_list)):
        Re = DE.reynoldsCalc(v_list[i], l_n)
        C_Ftu = 0.455 / (math.log10(Re))**2.58
        c_Dn = C_Ftu * (1 + k_f) * S_nwet / S_w
        c_Dn_list.append(c_Dn)
    
    DeltaC_D_list = [0.002, 0.002, 0.002] # pretty accurate

    return(c_Df_list, c_Dn_list, DeltaC_D_list)

# extract data from files and plot

c_Df_list = DragFactorsAlti(altitudes_list, v_list)[0]
c_Dn_list = DragFactorsAlti(altitudes_list, v_list)[1]
DeltaC_D_list = DragFactorsAlti(altitudes_list, v_list)[2]

for i in range(len(altitudes_list)):
    cd_all_list = ExtrParamTxt("Aircraft-Design_II/Wing_Polar_Graph_" + str(altitudes_list[i]) + "m.txt", "CD")
    cl_all_list = ExtrParamTxt("Aircraft-Design_II/Wing_Polar_Graph_" + str(altitudes_list[i]) + "m.txt", "CL")
    for j in range(len(cd_all_list)):
        cd_all_list[j] = cd_all_list[j] + c_Df_list[i] + c_Dn_list[i] + DeltaC_D_list[i]
    cl_cd_list = []
    for j in range(len(cd_all_list)):
        cl_cd_list.append(cl_all_list[j] / cd_all_list[j])
    plt.plot(cl_all_list, cl_cd_list, linestyle = "-", label = "h = " + str(altitudes_list[i]) + " m")
        
plt.xlabel("CL")
plt.ylabel("CL/CD")
plt.legend(loc='best')
plt.grid(True)
plt.show()
plt.close()