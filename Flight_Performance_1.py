# this script is referring to the tuwel document
# importing libaries
import Drag_AD2 as DAD2
import math
import constants as con
from wing_area import wing_parameter
import matplotlib.pyplot as plt
from isa import isa_model
import main
# level flight diagram
# required thrust-to-weight ratio
# calculation of equivalent airspeeds assuming level flight
# recycling cd and cl lists without compression drag
cd_list = DAD2.cd_indu_all_list
cl_list = DAD2.cl_indu_all_list
# creating an empty list for equivalent airspeeds
vEAS_list = []
# calculationg W/S at mTO
WS = main.Momenten_Summe['Weights'] * 9.81 / wing_parameter(con.AR,con.taper)[4] 
# equation for each element in cl list
for cl in cl_list:
    vEAS_list.append( math.sqrt(2 * WS / 1.225 / abs(cl)) )
# clipping the lists for negative cl
for i in range(len(cl_list)-1, -1, -1):
    if cl_list[i] < 0:
        cl_list.pop(i)
        cd_list.pop(i)
        vEAS_list.pop(i)
# calculate the reciprocal of the glide ratio D/L
dl_list = []
for i in range(len(cl_list)):
    dl_list.append(cd_list[i]/cl_list[i])
# plotting epsion over vEAS
plt.plot(vEAS_list, dl_list)
plt.xlabel(r"$v_{EAS}$ (m/s)")
plt.ylabel(r"$\epsilon = D/L = (L/D)^{-1}$ (-)")
plt.show()
# calculating the true air speed vTAS at cruising altitude
vTAS_list = []
for vEAS in vEAS_list:
    vTAS_list.append(vEAS / math.sqrt( isa_model(con.H_CRUISE, con.dt)[3] / 1.225 ))