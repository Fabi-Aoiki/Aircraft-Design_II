from colorsys import hls_to_rgb

import numpy as np

import constants as cons
import isa
from constants import pwsafetyfactor

dt = cons.dt

#aircraft parameter fixed
ar = cons.AR
n_e = cons.N_E

#cruise
h_cruise = cons.H_CRUISE

kc = 0.99
tr_thr = 0.8
n_trans = 0.99
n_prop = 0.9

cd0 = cons.cd0
e0 = cons.e0_cruise

kappa = 1/(np.pi * ar * e0)

m_cruise_max = cons.ma_max
v_cruise_max = m_cruise_max * isa.isa_model(h_cruise, dt)[3]

def calcPowerToWeightCruiseBase(ws):
    q = 0.5 * isa.isa_model(h_cruise, dt)[2] * v_cruise_max ** 2
    pw = (q * cd0 / ws + kappa * ws / q) * kc * v_cruise_max / (tr_thr * n_trans * n_prop)
    return pw

#cruise OEI
h_cruise_oei = cons.H_CRUISE_OEI

kappa_oei = 1.3 * kappa
tr_thr_oei = 0.95

def calcPowerToWeightCruiseBaseOEI(ws):
    q_oei = 0.5 * isa.isa_model(h_cruise, dt)[2] * v_cruise_max ** 2
    v_cruise_oei = np.sqrt(2 * q_oei / isa.isa_model(h_cruise_oei,dt)[2])
    epsilon_cruise_oei = q_oei * cd0 / ws + kappa_oei * ws / q_oei
    pw = epsilon_cruise_oei * kc * v_cruise_oei / (tr_thr_oei * n_trans * n_prop) * n_e / (n_e - 1)
    return pw

#take off OEI
g0 = 9.81
h_to = cons.h_TO
dt_to = cons.dT_TO
rho_0 = isa.isa_model(h_to, dt_to)[2]

nzw = 1 #load factor
n_ground = 0.03
n_aero_frict = 0.13
n_prop_to = 0.7
n_prop_to_oei = 0.8
tr_thr_to = 1
h_scr = 10.67

pwsafetyfactor = cons.pwsafetyfactor

cl_max_start = cons.c_Lmax_Start
cd0_to = cons.cd0_to
e0_to = cons.e_TO

kappa_to = 1/(np.pi * e0_to * ar)

def takeoff_speeds(ws):
    vsr = np.sqrt(2 * nzw * ws / (rho_0 * cl_max_start))
    v_lof = 1.08 * vsr
    v2 = 1.13 * vsr
    return vsr, v_lof, v2

def takeoff_pw_s1(s1, ws):
    v = 0.71 * takeoff_speeds(ws)[1]
    tw_s1 = 1.15 / (g0 * rho_0 * cl_max_start * s1 + (1 - 1 / (2 * n_e))) * ws / (1 - n_ground - n_aero_frict)
    pw_s1 = tw_s1 * v / (tr_thr_to * n_trans * n_prop_to)
    return pw_s1

def takeoff_pw_s3(s3, ws):
    v = 0.5 * (takeoff_speeds(ws)[1] + takeoff_speeds(ws)[2])
    q_to = 0.5 * rho_0 * v ** 2
    epsilon_to_oei = q_to * cd0_to / ws + kappa_to * ws / q_to
    tw_s3 = (np.sin(np.arctan(h_scr / s3)) + epsilon_to_oei) / (1 - 1 / n_e)
    pw_s3 = tw_s3 * v / (tr_thr_to * n_trans * n_prop_to_oei)
    return pw_s3

def takeOff_pw_ws(ws):
    datenpunkte = 200
    disList = []
    rollDisList = []
    climDisList = []
    diffList = []

    for i in range(0, datenpunkte - 1):
        s = 2200 / datenpunkte * (i + 1)
        disList.append(s)
        rollDisList.append(takeoff_pw_s1(s, ws))
        climDisList.append(takeoff_pw_s3(2200 - s, ws))
        diffList.append(round(abs(takeoff_pw_s1(s, ws) - takeoff_pw_s3(2200 - s, ws)), 2))

    indexmin = diffList.index(min(diffList))  # Gibt Listenindex mit kleinstem Wert aus

    return rollDisList[indexmin] * pwsafetyfactor

#Climbing Phase
v_v = 100 * 0.0058 #ft/min in m/s umgerechnet
h_max = cons.H_CRUISE

tr_thr_res_climb = 0.9
n_prop_res_climb = 0.9

def Climb_OEI_Out(ws):
    v = takeoff_speeds(ws)[2]
    q_to = 0.5 * rho_0 * v ** 2
    epsilon_out_oei = 0.8 * (q_to * cd0_to / ws + kappa_to * ws / q_to)
    pw_out_oei = (0.027 + epsilon_out_oei) * v / (tr_thr_to * n_trans * n_prop_to_oei) * n_e / (n_e - 1)
    return pw_out_oei

def Clim_Serv_out(ws):
    v = v_cruise_max
    q = 0.5 * isa.isa_model(h_max, dt)[2] * v ** 2
    epsilon_res_climb = q * cd0 / ws + kappa * ws / q
    pw = (v_v / v + epsilon_res_climb) * v / (tr_thr_res_climb * n_trans * n_prop_res_climb)
    return pw
