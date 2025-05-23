# this script is referring to the tuwel document
# importing libaries
import Drag_AD2 as DAD2
import math
# level flight diagram
# required thrust-to-weight ratio
# calculation of equivalent airspeeds assuming level flight
# recycling cd and cl lists without compression drag
cd_list = DAD2.cd_indu_all_list
cl_list = DAD2.cl_indu_all_list
# creating an empty list for equivalent airspeeds
vEAS_list = []
# equation for each element in cl list
for cl in cl_list:
    vEAS_list.append(  math.sqrt(2 * WS / 1.225 / cl)  )