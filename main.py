from PIL.GimpGradientFile import linear
from fontTools.misc.py23 import isclose

import constants
#from Take_Off_Distance import takeOff_pw_ws
from isa import isa_model
from Landing_Distance import getLandingDistance
from WS_Max import getWS_Max
import lhCalc
#from cruise import calcPowerToWeightCruiseBaseOEI, calcPowerToWeightCruiseBase
#from Climb_OEI_V1 import Climb_OEI_Out
#from Climb_service_V1 import Clim_Serv_out
from wing_area import phi_25_deg
from cruise import calcVCruise
#Test

from Test_Power_Calc import calcPowerToWeightCruiseBase, calcPowerToWeightCruiseBaseOEI, Climb_OEI_Out, Clim_Serv_out, takeOff_pw_ws, getWS_Max

import matplotlib.pyplot as plt
import numpy as np
import Prop_Dim_V1
import constants as con
import generalCalc
import Wing_thorenbeck
import Empenage_thorenbeck
import Fuselage_Thorenbeck
import Under_Thorenbeck
import Contro_Thorenbeck
import Engines_Thorenbeck
import Airframe_service_etc_Thorenbeck
import Seating_Thorenbeck
import mass_tank_and_insu
import pandas as pd


###############################################################################################################
#Dictoniary mit den Werten für die Summe

Momenten_Summe = {
    "Weights" : 0,
    "Mom_x" : 0,
    "Mom_z" : 0,
    "Mom_y" : 0,
}

Momenten_liste = {
    "Weights" : [],
    "Mom_x" : [],
    "L_x" : [],
    "Mom_z" : [],
    "L_z" : [],
    "Mom_y" : [],
    "L_y" : [],
}





class Moment:
    def __init__(self, Weight, X_Dis_m, Z_Dis_m = 0, Y_Dis_m = 0):

        self.Weight = float(Weight)
        self.x = float(X_Dis_m)
        self.z = float(Z_Dis_m)
        self.y = float(Y_Dis_m)

        self.Mom_x = self.x * self.Weight

        if self.z != 0:
            self.Mom_z = self.z * self.Weight
        else: self.Mom_z = 0

        if self.y != 0:
            self.Mom_y = self.y * self.Weight
        else: self.Mom_y = 0

        """if "Weights" not in self.dic.keys():
            self.dic["Weights"] = 0"""

        Momenten_Summe["Weights"] += self.Weight
        Momenten_Summe["Mom_x"] += self.Mom_x
        Momenten_Summe["Mom_z"] += self.Mom_z
        Momenten_Summe["Mom_y"] += self.Mom_y

        Momenten_liste["Weights"].append(self.Weight)
        Momenten_liste["Mom_x"].append(self.Mom_x)
        Momenten_liste["L_x"].append(self.x)
        Momenten_liste["Mom_z"].append(self.Mom_z)
        Momenten_liste["L_z"].append(self.z)
        Momenten_liste["Mom_y"].append(self.Mom_y)
        Momenten_liste["L_y"].append(self.y)



        




#Ws Stuff##############################################################################################



Values_Climb_OEI = []
Values_calcPowerToWeightCruiseBaseOEI = []
Values_calcPowerToWeightCruiseBase = []
Values_TO = []
Values_Clim_Serv_out = []
x_max = 9000#plot from 0 to this value
WS_Values = np.linspace(100,x_max,100)
mindiff = 1

for i in WS_Values:
    Values_Climb_OEI.append(Climb_OEI_Out(i))
    Values_calcPowerToWeightCruiseBaseOEI.append(calcPowerToWeightCruiseBaseOEI(i))
    Values_calcPowerToWeightCruiseBase.append(calcPowerToWeightCruiseBase(i))
    Values_TO.append(takeOff_pw_ws(i))
    Values_Clim_Serv_out.append(Clim_Serv_out(i))
    if (abs(calcPowerToWeightCruiseBase(i)-takeOff_pw_ws(i))<mindiff):
        minPWpoint = [i,calcPowerToWeightCruiseBase(i)]
        mindiff = abs(calcPowerToWeightCruiseBase(i)-takeOff_pw_ws(i))
        print(minPWpoint)
    #else:
        #print("FEHLER_00")


print(getLandingDistance())

#plotting############################################################################################

powerToWeightChosen = 20
x = WS_Values
plt.axvline(x = getWS_Max(), color='tab:grey', label='W/S Max', linestyle='dashdot')
#plt.axvline(x = getLandingDistance(), color='darkgreen', label='Landing Distance', linestyle='dashdot')
#plt.axvline(x = maxlandingWS, color='darkgreen', label='Landing Distance', linestyle='dashdot')
plt.axvline(x = 8860, color='darkgreen', label='Landing Distance', linestyle='dashdot')
plt.plot(x,Values_Clim_Serv_out, color='tab:green', label='Service Ceiling')
plt.plot(x, Values_Climb_OEI, color='tab:olive', label='Climb OEI')
plt.plot(x, Values_calcPowerToWeightCruiseBaseOEI, color='tab:cyan', label='Cruise OEI')
plt.plot(x, Values_calcPowerToWeightCruiseBase, color='tab:purple', label='Cruise')
plt.plot(x, Values_TO, color='tab:pink', label='Take-off')
plt.axhline(y=powerToWeightChosen, color='tab:orange', label='Selected P/W ratio', linestyle='--')
plt.scatter(minPWpoint[0], minPWpoint[1], color='tab:brown', label='Minimal Point', zorder=2)
plt.scatter(3300, powerToWeightChosen, color='tab:red', label='Design Point', zorder=2)
plt.xlim([0, x_max])
plt.ylim([0, 100])
plt.xlabel('Wing Loading [N/m^2]')
plt.ylabel('Power to Weight Ratio [W/N]')
plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05),ncol=3, fancybox=True, shadow=True)
plt.grid()
plt.show()

Prop_Base = Prop_Dim_V1.Prop_size(con.P_b)
Prop_Stretch = Prop_Dim_V1.Prop_size(con.P_s)

print("Prop_Base",Prop_Base)
print("Prop_Stretch",Prop_Stretch)

#calcs for lh ################################################################################################
P_elCr = lhCalc.calcElPower(lhCalc.FlightPhase.cruise, powerToWeightChosen)
P_elTo = lhCalc.calcElPower(lhCalc.FlightPhase.takeOff, powerToWeightChosen)
lhCalc.calcElPower(lhCalc.FlightPhase.climb, powerToWeightChosen)
P_stackDesign = lhCalc.calcDesignStackPower(P_elCr)
P_stackMax = lhCalc.calcStackPowerMax(P_stackDesign)
P_batMin = lhCalc.calcMinElPowBat(P_stackMax, powerToWeightChosen)
V_tankMinBase = lhCalc.calcMinTankVol(con.m_fBas)
V_tankMinStr = lhCalc.calcMinTankVol(con.m_fStr)
V_fcStackBase = lhCalc.calcStackVolume(P_stackDesign, 1-con.oversizingFc)
V_sys = lhCalc.calcSystemVolume(P_stackDesign, 1-con.oversizingFc)
V_Bat = lhCalc.calcVolBat(P_batMin)
dQdtCool = lhCalc.calcdQdTCool(P_elTo, 1)
V_cool = lhCalc.calcCoolingVolume(dQdtCool, 1)
W_Bat = lhCalc.calcMinWeightBat(P_batMin)
W_fcStackBase = lhCalc.calcStackWeight(P_stackDesign, 1-con.oversizingFc)
W_sys = lhCalc.calcSystemsWeight(P_stackDesign, 1-con.oversizingFc)
W_cool = lhCalc.calcCoolingWeight(dQdtCool, 1)
print("Elec Power Overall Cruise", P_elCr)
print("FC Stack Power Design", P_stackDesign)
print("FC Stack Power Max", P_stackMax)
print("Minimum Bat Power:", P_batMin)
print("Minimum Bat Volume:", V_Bat)
print("Minimum tank volume base: ", V_tankMinBase)
print("Minimum tank volume stretch: ", V_tankMinStr)
print("Minimum FC Stack volume: ", V_fcStackBase)
print("Minimum FC System volume: ", V_sys)
print("Minimum FC Cooling volume: ", V_cool)
print("Minimum FC Stack weight: ", W_fcStackBase)
print("Minimum FC System weight: ", W_sys)
print("Minimum FC Cooling weight: ", W_cool)
print("Minimum Bat Weight:", W_Bat)



#Weights Calculations######################################################################################################
W_Tank = mass_tank_and_insu.m_T_I_tot
print(f"Tank and Insu {W_Tank} [kg]")
M_Tank = Moment(W_Tank,29.893,0)

W_FC_Stack = W_fcStackBase 
print(f"FC Stuff {W_FC_Stack} [kg]")
M_FC_Stack = Moment(W_FC_Stack,31.716,-1.25)

W_FC_Sys = W_sys
print(f"FC Stuff {W_FC_Sys} [kg]")
M_FC_Sys = Moment(W_FC_Sys,31.716,-1.25)

W_FC_cool = W_cool
print(f"FC Stuff {W_FC_cool} [kg]")
M_FC_Cool = Moment(W_FC_cool,29.893,-2.025)

W_FC_Bat = W_Bat
print(f"FC Stuff {W_FC_Bat} [kg]")
M_FC_Bat = Moment(W_FC_Bat,28.396,-1.25)

Ww = Wing_thorenbeck.Calc_Ww()
print(f"Wing Weight nach Thorenbeck apendix C = {Ww} [kg]")
M_Ww = Moment(Ww*2,34.6,2.46)

W_tail = Empenage_thorenbeck.Calc_W_tail()
print(f"Empenage Weight nach Thorenbeck Kapitel 8 = {W_tail} [kg]")
M_Tail = Moment(W_tail,59.437,5.88)

W_fus = Fuselage_Thorenbeck.Calc_fus()
print(f"Fus Weight nach Thorenbeck Kapitel 8 + Apendix b d = {W_fus} [kg]")
M_fus = Moment(W_fus,28.215,0.1)

W_Nose_Gear = Under_Thorenbeck.Calc_under_Nose()
print(f"Nose Gear Weifght nach Thorenbeck Kapitel 8 = {W_Nose_Gear} [kg]")
M_Nose_Gear = Moment(W_Nose_Gear,5,-4)

W_Main_Gear = Under_Thorenbeck.Calc_under_Main()
print(f"Main Gear Weifght nach Thorenbeck Kapitel 8 = {W_Main_Gear} [kg]")
M_Main_Gear = Moment(W_Main_Gear,36.765,-4)

W_control = Contro_Thorenbeck.Calc_Wsc()
print(f"Control Weight nach Thorenbeck Kapitel 8 = {W_control} [kg]")
M_sc = Moment(W_control,38.382,2.459)

W_nacel = Engines_Thorenbeck.Calc_Wn()
print(f"Nacel Weight nach Thorenbeck Kapitel 8 = {W_nacel} [kg]")
M_Nac_Front = Moment(W_nacel/2,32.646,2.459)
M_Nac_Back = Moment(W_nacel/2,35.822,2.459)

W_engins = Engines_Thorenbeck.Calc_We()
print(f"Engine Weight nach Thorenbeck Kapitel 8 = {W_engins} [kg]")
M_Eng_Front = Moment(W_engins/2,32.646-1,2.459)
M_Eng_Back = Moment(W_engins/2,35.822-1,2.459)

Wieg = Airframe_service_etc_Thorenbeck.Calc_Wieg()
print(f"Instruments etc. Weight nach Thorenbeck Kapitel 8 = {Wieg} [kg]")
M_IEG = Moment(Wieg,7,1) # Educated Guess

Whp = Airframe_service_etc_Thorenbeck.Calc_Whp()
print(f"Hydraulics and pneumatics Weight nach Thorenbeck Kapitel 8 = {Whp} [kg]")
M_HP = Moment(Whp,40.867,1.229)

Wel = Airframe_service_etc_Thorenbeck.Calc_Wel()
print(f"Electrical Weight nach Thorenbeck Kapitel 8 = {Wel} [kg]")
M_EL = Moment(Wel,25.114,-0.5)

Wfur = Airframe_service_etc_Thorenbeck.Calc_Wfurn() # Berechnung 8.4.3.d nach Formel 8-44 oder nach Tabelle 8-12
print(f"Furniture Weight nach Thorenbeck Kapitel 8 = {Wfur} [kg]")
M_Fur = Moment(Wfur,29.893,1)

WAC = Airframe_service_etc_Thorenbeck.Calc_Weight_AC()
print(f"A.C. Weight nach Thorenbeck Kapitel 8 inklusive korrektur = {WAC} [kg]")
M_AC = Moment(WAC,21,-1.25)

W_seat_econ = Seating_Thorenbeck.Calc_Weight_econ()
print(f"Economy sitze nach Recaro {W_seat_econ} [kg]")
M_Seat_Econ = Moment(W_seat_econ,37.814,0.5)

W_seat_buis = Seating_Thorenbeck.Calc_Weight_Buisness()
print(f"Buisness sitze nach Recaro {W_seat_buis} [kg]")
M_Seat_Busi = Moment(W_seat_buis,13.658,0.5)







print(Momenten_Summe)
print(Momenten_liste)

# "Weights" : [],
#     "Mom_x" : [],
#     "L_x" : [],
#     "Mom_z" : [],
#     "L_z" : [],
#     "Mom_y" : [],
#     "L_y" : [],


# W_l = Momenten_liste['Weights']
# M_x_l = Momenten_liste['Mom_x']
# L_x_l = Momenten_liste["L_x"]
# M_z_l = Momenten_liste['Mom_z']
# L_z_l = Momenten_liste["L_z"]
# M_y_l = Momenten_liste['Mom_y']
# L_y_l = Momenten_liste["L_y"],

Data_0 ={'Weights': Momenten_liste['Weights'],
     'Momente_X': Momenten_liste['Mom_x'],
     'L_x': Momenten_liste["L_x"],
     'Momente_Z': Momenten_liste['Mom_z'],
     'L_z': Momenten_liste["L_z"],
     'Momente_y': Momenten_liste['Mom_y'],
     'L_y': Momenten_liste["L_y"],
      }
df_0 = pd.DataFrame.from_dict(Momenten_liste)



df_0.to_excel('Momente.xlsx', sheet_name='Calculation', index=False,)

df_1 = pd.DataFrame({'Weights': Momenten_Summe['Weights'],
        'Momente_X': Momenten_Summe['Mom_x'],
        'Momente_Z': Momenten_Summe['Mom_z'],
        'Momente_y': Momenten_Summe['Mom_y'],
        },
        index=(10,20,30,40)
    )  


df_1.to_excel('Momenten_summen.xlsx', sheet_name='Summen')


d = {'WS': getWS_Max(), 'v_s': calcVCruise(), 'v_m': con.ma, 'AR' : con.AR, 'taper' : con.taper, 'Mto' : (con.Wto /9.81)/1000, 'sweep': phi_25_deg}
ser = pd.Series(data=d, index=['WS', 'v_s', 'v_m', 'AR', 'taper', 'Mto', 'sweep'])

ser.to_excel('values.xlsx', sheet_name='Calc')




#Main Longer
