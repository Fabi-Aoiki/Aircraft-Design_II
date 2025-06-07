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
# import LD_CL_Calc as LDCL
import ld_cl_calc_NEW as LDCL
import numpy as np
from scipy.interpolate import make_interp_spline
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
plt.close()
# calculate the reciprocal of the glide ratio D/L
dl_list = []
for i in range(len(cl_list)):
    dl_list.append(cd_list[i]/cl_list[i])
# plotting epsilon over vEAS
plt.plot(vEAS_list, dl_list)
plt.xlabel(r"$v_{EAS}$ (m/s)")
plt.ylabel(r"$\epsilon = D/L = (L/D)^{-1}$ (-)")
# plt.show()
plt.close()
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
# plt.show()
plt.close()
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
# plt.show()
plt.close()
# once again but over Mach since it looks way better
plt.plot(Ma_list, dl_list, label = "w/o compr drag")
plt.plot(Ma_list, dl_compr_list, label = "w/ compr drag")
plt.xlabel(r"M (-)")
plt.ylabel(r"$\epsilon = D/L = (L/D)^{-1}$ (-)")
plt.ylim(0,1)
plt.xlim(min(Ma_list)*0.9, 1)
plt.legend()
# plt.show()
plt.close()

# available thrust-to-weight ratio
# calculations for a turbofan
# first equation of page 5 from 20
# throttle ratio not sure need to ask fabi or georg
# no idea with the units but i just go with the flow
thrust_list = []
for Ma in Ma_list:
    thrust_list.append( con.TRthr_CR * ( isa_model(con.H_CRUISE, con.dt)[2] / 1.225 ) * \
                        math.exp( -0.35 * Ma * ( isa_model(con.H_CRUISE, con.dt)[2] / 101325 ) * math.sqrt( 60 ) ) )
# now just mutliplying the second equation inside there
for i in range(len(thrust_list)):
    thrust_list[i] = thrust_list[i] * ( 1 - ( 1.3 + 0.25 * 60 ) * 0.02 ) 
# multiplying with the installed static thrust-to-weight ratio and the current weight ratio
# taking thrust for FL400 at Mach 0 for mass closer after take-off
# times 4 at the end because of four propellers that apply to one parameter
for i in range(len(thrust_list)):
    thrust_list[i] = thrust_list[i] * am.perf_5[0][0] / ( main.W_Take_off * 9.81 * 0.99 ) * 16
# plotting the result
plt.plot(Ma_list, dl_compr_list, label = "required")
plt.plot(Ma_list, thrust_list, label = "available")
plt.xlabel(r"M")
plt.ylabel(r"$\epsilon = D/L = (L/D)^{-1}$ (-)")
plt.ylim(0,1)
plt.xlim(0.5, 1)
plt.legend()
plt.show()

# climb perfomance
# specific excess thrust
# left side minus right side
# altitudes 0, 2500, 5000, 7500, 10000, 12000 metres
perf_list = [am.perf_0, am.perf_1, am.perf_2, am.perf_3, am.perf_4, am.perf_5]
alti_list = [0, 2500, 5000, 7500, 10000, 12000]
gamma_list_all = []
mach_list_all = []
epsilon_list_all = []
# iterate through all the altitudes
for k in range(6):
    # min and max mach for the altitude
    minMach = min(LDCL.Calc_LD_M()[0][k])
    maxMach = max(LDCL.Calc_LD_M()[0][k])
    # approximate as functions (5th order polynomial) for left side
    koeff = np.polyfit(perf_list[k][4], perf_list[k][0], 5)
    # calculating the left side
    left_side_values = []
    for i in np.arange(minMach, maxMach+0.01, 0.01):
        # evaluating function
        value = 0
        for j in range(len(koeff)):
            value = value + koeff[j] * i ** (len(koeff)-1-j)
        value = value * 4 * 0.9 / (main.W_Take_off * 9.81)
        left_side_values.append(value)
    # calculating the right side
    koeff = np.polyfit(LDCL.Calc_LD_M()[0][k], LDCL.Calc_LD_M()[1][k], 5)
    right_side_values = []
    for i in np.arange(minMach, maxMach+0.01, 0.01):
        # evaluating function
        value = 0
        for j in range(len(koeff)):
            value = value + koeff[j] * i ** (len(koeff)-1-j)
        print(value)
        value = 1 / value
        right_side_values.append(value)
    # calculating the difference for gamma
    gamma = []
    for i in range(len(right_side_values)):
        gamma.append(left_side_values[i] - right_side_values[i])
    mach_list_all.append(np.arange(minMach, maxMach+0.01, 0.01))
    gamma_list_all.append(gamma)
    epsilon_list_all.append(right_side_values)
# plotting for all altitudes
for i in range(len(mach_list_all)):
    plt.plot(mach_list_all[i], gamma_list_all[i], label = "h = " + str(alti_list[i]) + " m")
plt.xlabel("M (-)")
plt.ylabel(r"$\gamma$ (rad)")
plt.xlim(0, 0.85) # otherwise you cannot see anything
plt.ylim(0, max(gamma_list_all[0])) # need that because of xlim
plt.legend()
plt.show()
plt.close()
# converting from Mach to vTAS
vTAS_list_all = []
for j in range(len(alti_list)):
    vTAS_list = []
    for i in range(len(mach_list_all[j])):
        vTAS_list.append( mach_list_all[j][i] * isa_model(alti_list[j], 0)[3] )
    vTAS_list_all.append(vTAS_list)
# plotting for all altitudes but now with TAS
for i in range(len(vTAS_list_all)):
    plt.plot(vTAS_list_all[i], gamma_list_all[i], label = "h = " + str(alti_list[i]) + " m")
plt.xlabel("$v_{TAS}$ (m/s)")
plt.ylabel(r"$\gamma$ (rad)")
plt.legend()
plt.title("Specific Excess Thrust (Climb)")
plt.xlim(0, 251) # otherwise you cannot see anything
plt.ylim(0, max(gamma_list_all[0])) # need that because of xlim
plt.show()
plt.close()
# climb: Specific Excess Power
SEP_list_all = []
for i in range(len(alti_list)):
    SEP_list = []
    for j in range(len(gamma_list_all[i])):
        SEP_list.append( vTAS_list_all[i][j] * gamma_list_all[i][j] )
    SEP_list_all.append(SEP_list)
# plotting for all altitudes
for i in range(len(vTAS_list_all)):
    plt.plot(vTAS_list_all[i], SEP_list_all[i], label = "h = " + str(alti_list[i]) + " m")
plt.xlabel("$v_{TAS}$ (m/s)")
plt.ylabel("SEP (m/s)")
plt.legend()
plt.title("Specific Excess Power (Climb)")
plt.xlim(0, 251) # otherwise you cannot see anything
plt.ylim(0, max(SEP_list_all[0])) # need that because of xlim
plt.show()
plt.close()
# specific air range (sar) for hydrogen
# values need to be updated once available
heating_value = 120 * 10**6
eta_approx = 0.9**6
weight = main.W_Take_off * 9.81
# iterate over alts
SAR_list_all = []
for i in range(len(epsilon_list_all)):
    SAR_list = []
    for j in range(len(epsilon_list_all[i])):
        SAR = eta_approx / epsilon_list_all[i][j] / weight * heating_value
        SAR_list.append(SAR)
    SAR_list_all.append(SAR_list)
# plotting for all altitudes
for i in range(len(SAR_list_all)):
    plt.plot(vTAS_list_all[i], SAR_list_all[i], label = "h = " + str(alti_list[i]) + " m")
plt.xlabel("$v_{TAS}$ (m/s)")
plt.ylabel("SAR (m/kg)")
plt.legend()
plt.title("Specific Air Range")
plt.xlim(0, 251) # otherwise you cannot see anything
plt.ylim(0, max(SAR_list_all[-1])*1.2) # need that because of xlim
plt.show()
plt.close()
# optimum velocities
# need to find the maximum for SET, SEP and SAR at each alt
# setting the right name for the SET (gamma) list
SET_list_all = gamma_list_all
# for each altitude
vTAS_Max_SET_list = []
for i in range(len(SET_list_all)):
    index_of_max = SET_list_all[i].index(max(SET_list_all[i]))
    max_speed = vTAS_list_all[i][index_of_max]
    vTAS_Max_SET_list.append(max_speed)
vTAS_Max_SEP_list = []
for i in range(len(SEP_list_all)):
    index_of_max = SEP_list_all[i].index(max(SEP_list_all[i]))
    max_speed = vTAS_list_all[i][index_of_max]
    vTAS_Max_SEP_list.append(max_speed)
vTAS_Max_SAR_list = []
for i in range(len(SAR_list_all)):
    index_of_max = SAR_list_all[i].index(max(SAR_list_all[i]))
    max_speed = vTAS_list_all[i][index_of_max]
    vTAS_Max_SAR_list.append(max_speed)
# plotting
plt.plot(vTAS_Max_SET_list, alti_list, label = r"$SET_{max}$")
plt.plot(vTAS_Max_SEP_list, alti_list, label = r"$SEP_{max}$")
plt.plot(vTAS_Max_SAR_list, alti_list, label = r"$SAR_{max}$")
plt.xlabel(r"$v_{TAS}$ (m/s)")
plt.ylabel("altitude (m)")
plt.title("Optimum Velocities")
plt.legend()
plt.show()
plt.close()
# specific flight time
# for hydro simply use SAR and devide through speed
SE_list_all = []
for i in range(len(SAR_list_all)):
    SE_list = []
    for j in range(len(SAR_list_all[i])):
        SE_list.append( SAR_list_all[i][j] / vTAS_list_all[i][j] )
    SE_list_all.append(SE_list)
# plotting
for i in range(len(SE_list_all)):
    plt.plot(vTAS_list_all[i], SE_list_all[i], label = "h = " + str(alti_list[i]) + " m")
plt.xlabel("$v_{TAS}$ (m/s)")
plt.ylabel("SE (s/kg)")
plt.legend()
plt.title("Specific Flight Time")
plt.show()
plt.close()