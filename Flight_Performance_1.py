# this script is referring to the tuwel document
# importing libaries
import Drag_AD2 as DAD2
import math
import constants as con
from wing_area import wing_parameter
import matplotlib.pyplot as plt
from isa import isa_model
import main
import axial_momentum as am
# level flight diagram
# required thrust-to-weight ratio
# calculation of equivalent airspeeds assuming level flight
# recycling cd and cl lists without compression drag
# creating a copy so the DAD2 lists are not changes
cd_list = DAD2.cd_indu_all_list.copy()
cl_list = DAD2.cl_indu_all_list.copy()
# creating an empty list for equivalent airspeeds
vEAS_list = []
# calculationg W/S at mTO
WS = main.W_Take_off * 9.81 / wing_parameter(con.AR,con.taper)[4] 
# equation for each element in cl list
for cl in cl_list:
    vEAS_list.append( math.sqrt( 2 * WS / 1.225 / abs(cl) ) )
# clipping the lists for negative cl
for i in range(len(cl_list)-1, -1, -1):
    if cl_list[i] < 0:
        cl_list.pop(i)
        cd_list.pop(i)
        vEAS_list.pop(i)
# plotting cl over cd just to check how it looks like
plt.plot(cd_list, cl_list)
plt.xlabel("CD")
plt.ylabel("CL")
plt.show()
# calculate the reciprocal of the glide ratio D/L
dl_list = []
for i in range(len(cl_list)):
    dl_list.append(cd_list[i]/cl_list[i])
# plotting epsilon over vEAS
plt.plot(vEAS_list, dl_list)
plt.xlabel(r"$v_{EAS}$ (m/s)")
plt.ylabel(r"$\epsilon = D/L = (L/D)^{-1}$ (-)")
plt.show()
# calculating the true air speed vTAS at cruising altitude
vTAS_list = []
for vEAS in vEAS_list:
    vTAS_list.append(vEAS / math.sqrt( isa_model(con.H_CRUISE, con.dt)[2] / 1.225 ))
# calculating the flight mach number
Ma_list = []
for vTAS in vTAS_list:
    Ma_list.append(vTAS / isa_model(con.H_CRUISE, con.dt)[3])
# we assume that wing lift is airplane lift
# calculating the drag divergence mach number for the wing
MaDD_list = []
kFac_list = [0.758, 0.1, -0.09, 0, -0.1]
for cl in cl_list:
    MaDDj = 0
    for i in range(len(kFac_list)):
        MaDDj = MaDDj + kFac_list[i] * cl ** i
    MaDD_list.append( MaDDj )
# plotting lift over mach to check how it looks
plt.plot(MaDD_list, cl_list)
plt.xlabel("Ma Drag Divergence")
plt.ylabel("CL")
plt.ylim(0, max(cl_list)*1.1)
plt.xlim(0, max(MaDD_list)*1.1)
plt.show()
# calculating ΔM for the compressible drag
DeltaM_list = []
for i in range(len(Ma_list)):
    DeltaM_list.append( Ma_list[i] - MaDD_list[i] / math.sqrt( math.cos( 21.4 * math.pi / 180 ) ) )
# calculating the compressible drag
DeltaDrag_list = []
for DeltaM in DeltaM_list:
    DeltaDrag_list.append( 0.002 * math.exp( 60 * DeltaM ) )
# calculating the total drag
cd_compr_list = []
for i in range(len(cd_list)):
    cd_compr_list.append( cd_list[i] + DeltaDrag_list[i] )
# creating dl (epsilon) list again now with compression
dl_compr_list = []
for i in range(len(cd_compr_list)):
    dl_compr_list.append( cd_compr_list[i] / cl_list[i] )
# creating plot
plt.plot(vEAS_list, dl_list, label = "w/o compr drag")
plt.plot(vEAS_list, dl_compr_list, label = "w/ compr drag")
plt.xlabel(r"$v_{EAS}$ (m/s)")
plt.ylabel(r"$\epsilon = D/L = (L/D)^{-1}$ (-)")
plt.ylim(0,1)
plt.xlim(min(vEAS_list)*0.9, 320)
plt.legend()
plt.show()


# available thrust-to-weight ratio
# calculations for a turbofan
# first equation of page 5 from 20
# throttle ratio not sure need to ask fabi or georg
# no idea with the units but i just go with the flow
thrust_list = []
for Ma in Ma_list:
    thrust_list.append( 0.8 * (1.225 / isa_model(con.H_CRUISE, con.dt)[2]) * \
                        math.exp( -0.35 * Ma * ( isa_model(con.H_CRUISE, con.dt)[2] / 101325 ) * math.sqrt( am.Pbr ) ) )
# now just mutliplying the second equation inside there
for i in range(len(thrust_list)):
    thrust_list[i] = thrust_list[i] * ( 1 - ( 1.3 + 0.25 * am.Pbr ) * 0.02 ) 
# multiplying with the installed static thrust-to-weight ratio and the current weight ratio
# i have no idea what those values are to be honest
# need to ask fabi or georg about that
for i in range(len(thrust_list)):
    thrust_list[i] = thrust_list[i] * 1.0 * 1.0
# plotting the result
# diagram is still fucked up obviously
plt.plot(vEAS_list, dl_compr_list, label = "required")
plt.plot(vEAS_list, thrust_list, label = "available")
plt.xlabel(r"$v_{EAS}$ (m/s)")
plt.ylabel(r"$\epsilon = D/L = (L/D)^{-1}$ (-)")
plt.ylim(0,1)
plt.xlim(min(vEAS_list)*0.9, 320)
plt.legend()
plt.show()